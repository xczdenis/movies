from dataclasses import dataclass
from typing import Optional, Type

import orjson
from db.interface import IAsyncCacheStorage, IAsyncDB
from loguru import logger
from pydantic import BaseModel
from services.utils import make_key_from_args


@dataclass
class BaseAPIService:
    db: IAsyncDB
    cache_db: IAsyncCacheStorage

    async def get(self, model: Type[BaseModel], object_id: str, **kwargs) -> Optional[BaseModel]:
        by_alias = kwargs.get("by_alias", False)
        cache_key = await make_key_from_args(model=model, object_id=object_id, _solt="detail", **kwargs)
        model_instance = None

        data_from_cache = await self.cache_db.get(key=cache_key, **kwargs)
        if not data_from_cache:
            logger.debug(f"The data was not found in the cache (key: {cache_key})")

            model_instance = await self.db.get(model=model, id=object_id, **kwargs)
            if model_instance:
                await self.cache_db.set(cache_key, model_instance.json(by_alias=by_alias), **kwargs)
        else:
            model_instance = model.parse_raw(data_from_cache)

        return model_instance

    async def all(self, model: Type[BaseModel], **kwargs) -> tuple[int, list[BaseModel]]:
        by_alias = kwargs.get("by_alias", False)

        total_objects_in_db = 0
        model_instances = []

        cache_key = await make_key_from_args(model=model, _solt="all", **kwargs)
        data_from_cache = await self.cache_db.get(cache_key, **kwargs)

        if not data_from_cache:
            logger.debug(f"The data was not found in the cache (key: {cache_key})")

            total_objects_in_db, model_instances = await self.db.search(model=model, **kwargs)
            if model_instances:
                data_for_cache = [instance.json(by_alias=by_alias) for instance in model_instances]
                await self.cache_db.set(cache_key, orjson.dumps(data_for_cache), **kwargs)
        else:
            total_objects_in_db = await self.db.count(model=model, **kwargs)
            parsed_data_from_cache = orjson.loads(data_from_cache)
            if isinstance(parsed_data_from_cache, list):
                model_instances = [model.parse_raw(item) for item in parsed_data_from_cache]

        return total_objects_in_db, model_instances
