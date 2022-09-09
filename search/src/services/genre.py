from dataclasses import dataclass
from typing import Optional

from db.cache import get_cache_db
from db.db import get_db
from db.interface import IAsyncCacheStorage, IAsyncDB
from fastapi import Depends
from models.genre import Genre
from services.base import BaseAPIService


@dataclass
class GenreService:
    api_service: BaseAPIService

    async def get(self, object_id: str, **kwargs) -> Optional[Genre]:
        return await self.api_service.get(model=Genre, object_id=object_id, **kwargs)

    async def all(self, **kwargs) -> tuple[int, list[Genre]]:
        return await self.api_service.all(model=Genre, **kwargs)


# @lru_cache()
def get_genre_service(
    cache_db: IAsyncCacheStorage = Depends(get_cache_db),
    db: IAsyncDB = Depends(get_db),
) -> GenreService:
    return GenreService(BaseAPIService(cache_db=cache_db, db=db))
