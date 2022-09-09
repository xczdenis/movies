from typing import Optional

from db.interface import IAsyncCacheStorage

cache_db: Optional[IAsyncCacheStorage] = None


async def get_cache_db() -> IAsyncCacheStorage:
    return cache_db
