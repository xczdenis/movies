from dataclasses import dataclass
from typing import Optional

from db.cache import get_cache_db
from db.db import get_db
from db.interface import IAsyncCacheStorage, IAsyncDB
from fastapi import Depends
from models.film import Film
from models.person import Person
from services.base import BaseAPIService


@dataclass
class PersonService:
    api_service: BaseAPIService

    async def get(self, object_id: str, **kwargs) -> Optional[Person]:
        return await self.api_service.get(model=Person, object_id=object_id, **kwargs)

    async def all(self, **kwargs) -> tuple[int, list[Person]]:
        return await self.api_service.all(model=Person, **kwargs)

    async def all_films_by_person(self, **kwargs) -> tuple[int, list[Film]]:
        return await self.api_service.all(model=Film, **kwargs)


# @lru_cache()
def get_person_service(
    cache_db: IAsyncCacheStorage = Depends(get_cache_db),
    db: IAsyncDB = Depends(get_db),
) -> PersonService:
    return PersonService(BaseAPIService(cache_db=cache_db, db=db))
