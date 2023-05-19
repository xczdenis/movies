from typing import Optional

from content.db.interfaces import AsyncCacheStorage

cache_db: Optional[AsyncCacheStorage] = None


async def get_cache_db() -> AsyncCacheStorage:
    return cache_db
