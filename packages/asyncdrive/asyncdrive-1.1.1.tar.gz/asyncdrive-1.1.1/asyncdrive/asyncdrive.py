import aiohttp
import asyncio
import datetime
import io
import json
import os

from pathlib import Path
from .utils import create_jwt

parent_directory = Path(__file__).resolve().parent

# if not os.path.exists(f"{parent_directory}/asyncache"):
#     os.makedirs(f"{parent_directory}/asyncache")


class AsyncRequest:

    def __init__(self, drive, *args, **kwargs):
        self.drive = drive
        self.args = args
        self.kwargs = kwargs

    async def __aenter__(self):
        await asyncio.sleep(self.drive.concurrent_requests // self.drive.ratelimit)
        async with self.drive.lock:
            await self.drive.ensure_valid_token()
        self.request = await self.drive.session.request(*self.args, **self.kwargs)
        return self.request

    async def __aexit__(self, type, value, traceback):
        try:
            if str(self.request.status)[0] != '2':
                raise Exception(
                    "Error {}: {}".format(self.request.status, await self.request.content.read()),
                    f"Request: {self.args} {self.kwargs}, ",
                    f"Headers: {self.drive.session._default_headers}"
                )
            elif traceback:
                raise Exception(traceback)
        finally:
            self.drive.concurrent_requests -= 1
            self.request.close()


class AsyncFile:

    def __init__(self, drive, file_name, mode='r'):
        MODES = ['r', 'r+', 'rb', 'rb+', 'w', 'w+', 'wb', 'wb+']
        if mode not in MODES:
            raise Exception(f"Unsupported mode '{mode}'")

        self.drive = drive
        self.mode = mode

        self.metadata_ = {'name': file_name}

    @property
    def file_name(self):
        return self.metadata_['name']

    @property
    def cache_location(self):
        return f'{parent_directory}/asyncache/{self.file_name}'

    async def __aenter__(self):
        file_list = json.loads(await self.drive.list(q=f"name = '{self.file_name}'"))['files'] + [{}]
        self.file_id = file_list[0].get('id', None)

        if 'w' in self.mode:
            self.file = io.BytesIO() if 'b' in self.mode else io.StringIO()

        elif self.file_id:
            if self.drive.cache and os.path.exists(self.cache_location):
                with io.open(self.cache_location, self.mode) as file:
                    content = file.read()
                    self.file = io.BytesIO(content) if 'b' in self.mode else io.StringIO(content)
            else:
                bytes = await self.drive.get(self.file_id)
                self.file = io.BytesIO(bytes) if 'b' in self.mode else io.StringIO(bytes.decode('utf-8'))
        else:
            raise FileNotFoundError(f"File {self.file_name} not found")

        return self

    async def __aexit__(self, type, value, traceback):
        try:
            if not traceback:
                if self.drive.cache:
                    self.cache_file(self.file.getvalue())

                if hasattr(self, 'pending_delete'):
                    # print('Deleting file:', self.file_name)
                    await self.drive.delete(self.file_id)

                elif 'w' in self.mode and not self.file_id:
                    # print('Creating file:', self.file_name)
                    await self.drive.create(self.file.getvalue(), **self.metadata_)

                elif any(item in self.mode for item in ['w', '+']) and self.file_id:
                    # print('Updating file:', self.file_name)
                    await self.drive.update(self.file_id, self.file.getvalue(), **self.metadata_)
            else:
                raise Exception(traceback)
        finally:
            self.file.close()

    def __getattr__(self, attr):
        return getattr(self.file, attr)

    def metadata(self, *_, **kwargs):
        for key, value in kwargs.items():
            self.metadata_[key] = value

    def cache_file(self, value):
        if not os.path.exists(f"{parent_directory}/asyncache"):
            os.makedirs(f"{parent_directory}/asyncache")
        with io.open(self.cache_location, 'wb' if 'b' in self.mode else 'w') as file:
            file.write(value)

    def delete(self):
        if 'w' in self.mode or '+' in self.mode:
            self.pending_delete = True
        else:
            raise Exception("Cannot delete read-only file")


class AsyncDrive:

    def __init__(self, cred_path, scopes, sub=None, ratelimit=10, cache=True):
        self.cred_path = cred_path
        self.scopes = scopes
        self.sub = sub
        self.ratelimit = ratelimit
        self.cache = cache

        self.session = aiohttp.ClientSession()
        self.lock = asyncio.Lock()
        self.token = None
        self.token_expiration_time = None
        self.concurrent_requests = 0

        self.pending_requests = []

    async def refresh_token(self):
        PAYLOAD = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": create_jwt(self.cred_path)
        }
        self.token_expiration_time = datetime.datetime.now().timestamp() + 3500

        async with self.session.post(url="https://oauth2.googleapis.com/token",
                                params={"content-Type": "application/x-www-form-urlencoded"},
                                data=PAYLOAD) as response:
            self.token = json.loads(await response.text())["access_token"]
            self.session._default_headers = {'Authorization': f'Bearer {self.token}'}

    async def ensure_valid_token(self):
        if self.token:
            if datetime.datetime.now().timestamp() < self.token_expiration_time:
                return
        await self.refresh_token()

    def request(self, *args, **kwargs):
        self.concurrent_requests += 1
        return AsyncRequest(self, *args, **kwargs)

    async def get(self, fileId):
        request_data = {
            'method': 'GET',
            'url': f'https://www.googleapis.com/drive/v3/files/{fileId}?alt=media'
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def list(self, *_, **params):
        if 'q' in params:
            params['q'] = params['q'].replace(' ', '+').replace('=', '%3d').replace('\'', '%27')
        params = '?' + '&'.join('{}={}'.format(k,v) for k,v in params.items())
        request_data = {
            'method': 'GET',
            'url': f'https://www.googleapis.com/drive/v3/files{params}'
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def delete(self, fileId):
        request_data = {
            'method': 'DELETE',
            'url': f'https://www.googleapis.com/drive/v2/files/{fileId}'
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def create(self, filePath, *_, **kwargs):
        data, headers = self.multipart_request(
            filePath,
            kwargs if kwargs else {'name': filePath, 'mimeType': 'application/octet-stream'}
        )
        request_data = {
            'method': 'POST',
            'url': 'https://www.googleapis.com/upload/drive/v3/files',
            'headers': headers,
            'data': data
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    async def update(self, fileId, filePath=None, *_, **kwargs):

        # Multipart upload
        if filePath and kwargs:
            data, headers = self.multipart_request(filePath, kwargs)

        # Simple upload
        elif filePath:
            data, headers = self.media_request(filePath)

        # Metadata-only upload
        elif kwargs:
            data, headers = self.metadata_request(kwargs)

        request_data = {
            'method': 'PATCH',
            'url': f"https://www.googleapis.com/{'upload/' if filePath else ''}drive/v3/files/{fileId}",
            'params': f"uploadType={'multipart' if kwargs else 'media'}" if filePath else '',
            'headers': headers,
            'data': data
        }
        async with self.request(**request_data) as response:
            return await response.content.read()

    def open(self, file_name, mode='r'):
        return AsyncFile(self, file_name, mode)

    def metadata_request(self, metaData):
        metadata = json.dumps(metaData).encode('utf-8')
        headers = {
             'Content-Length': str(len(metadata)),
             'Content-Type': 'application/json'
        }
        return metadata, headers

    def media_request(self, filePath):
        # with open(filePath, 'rb') as file:
        #     data = file.read()
        if type(filePath) == str:
            file_data = bytes(filePath, encoding='utf-8')
        else:
            file_data = filePath
        headers = {
            'Content-Length': str(len(data)),
            'Content-Type': 'application/octet-stream'
        }
        return data, headers

    def multipart_request(self, filePath, metaData):
        # with open(filePath, "rb") as file:
        #     file_data = file.read()
        if type(filePath) == str:
            file_data = bytes(filePath, encoding='utf-8')
        else:
            file_data = filePath

        boundary = b"------123456"
        delim = b"\n--" + boundary + b"\n"
        closing = b"\n--" + boundary + b"--"

        data = delim + \
            b"Content-Type: application/json; charset=UTF-8\n\n" + \
            json.dumps(metaData).encode("utf-8") + \
            delim + \
            b"Content-Type: " + metaData.get("mimeType", "application/octet-stream").encode("utf-8") + b"\n\n" + \
            file_data + closing

        headers = {
            "Content-Type": "multipart/related; boundary='" +
            boundary.decode("utf-8") + "'",
            "Content-Length": str(len(data))
        }
        return data, headers
