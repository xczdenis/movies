from dataclasses import dataclass

from fastapi import Depends

from content.api.dependencies.cache import get_cache_db
from content.api.dependencies.db import get_db
from content.db.interfaces import AsyncCacheStorage, AsyncDB
from content.models.film import Film
from content.models.person import Person
from content.services.base import BaseAPIService


@dataclass
class PersonService:
    api_service: BaseAPIService

    async def get(self, object_id: str, **kwargs) -> Person | None:
        return await self.api_service.get(model=Person, object_id=object_id, **kwargs)

    async def all(self, **kwargs) -> tuple[int, list[Person]]:
        return await self.api_service.all(model=Person, **kwargs)

    async def all_films_by_person(self, **kwargs) -> tuple[int, list[Film]]:
        return await self.api_service.all(model=Film, **kwargs)


# @lru_cache()
def get_person_service(
    cache_db: AsyncCacheStorage = Depends(get_cache_db),
    db: AsyncDB = Depends(get_db),
) -> PersonService:
    return PersonService(BaseAPIService(cache_db=cache_db, db=db))
