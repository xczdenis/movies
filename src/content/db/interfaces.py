from abc import ABC, abstractmethod
from typing import Awaitable, Optional, Type

from pydantic import BaseModel

from content.db.types import TEncodable


class AsyncDB(ABC):
    @abstractmethod
    async def get(self, model: Type[BaseModel], id: str, **kwargs) -> Optional[BaseModel]:
        pass

    @abstractmethod
    async def search(self, model: Type[BaseModel], **kwargs) -> tuple[int, list[BaseModel]]:
        pass

    @abstractmethod
    async def count(self, model: Type[BaseModel], **kwargs) -> int:
        pass

    @abstractmethod
    async def close(self):
        pass


class AsyncCacheStorage(ABC):
    @abstractmethod
    def get(self, key: str, **kwargs) -> Awaitable:
        pass

    @abstractmethod
    async def set(self, key: str, value: TEncodable, **kwargs):
        pass

    @abstractmethod
    async def close(self):
        pass
