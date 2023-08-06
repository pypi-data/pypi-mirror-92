import asyncio
import yaml
import json

from asyncdrive import AsyncDrive

drive = AsyncDrive(
    'test/test_creds.json',
    ['https://www.googleapis.com/auth/drive'],
    ratelimit=10,
    cache=True
)

async def main():
    d = {"test": "this\nis\na\ntest"}
    # with open('test.txt', 'w') as file:
    #     print(type(file))
    async with drive.open('yaml-test.yaml', 'r') as file:
        print(yaml.load(file))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
