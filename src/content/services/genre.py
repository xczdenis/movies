from dataclasses import dataclass

from fastapi import Depends

from content.api.dependencies.cache import get_cache_db
from content.api.dependencies.db import get_db
from content.db.interfaces import AsyncCacheStorage, AsyncDB
from content.models.genre import Genre
from content.services.base import BaseAPIService


@dataclass
class GenreService:
    api_service: BaseAPIService

    async def get(self, object_id: str, **kwargs) -> Genre | None:
        return await self.api_service.get(model=Genre, object_id=object_id, **kwargs)

    async def all(self, **kwargs) -> tuple[int, list[Genre]]:
        return await self.api_service.all(model=Genre, **kwargs)


# @lru_cache()
def get_genre_service(
    cache_db: AsyncCacheStorage = Depends(get_cache_db),
    db: AsyncDB = Depends(get_db),
) -> GenreService:
    return GenreService(BaseAPIService(cache_db=cache_db, db=db))
