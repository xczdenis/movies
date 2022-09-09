from typing import Awaitable

import aioredis
from aioredis import Redis as RedisClient
from db.interface import IAsyncCacheStorage
from db.types import TEncodable

CACHE_EXPIRE_IN_SECONDS = 60 * 5


class RedisStorage(IAsyncCacheStorage):
    def __init__(self, host: str, port: int):
        self.__client: RedisClient = aioredis.from_url(f"redis://{host}:{port}")

    def get(self, key: str, **kwargs) -> Awaitable:
        return self.__client.get(key)

    async def set(self, key: str, value: TEncodable, **kwargs):
        ex = kwargs.get("ex", CACHE_EXPIRE_IN_SECONDS)
        await self.__client.set(key, value, ex=ex)

    async def close(self):
        await self.__client.close()
