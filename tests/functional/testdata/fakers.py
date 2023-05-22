import json
from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch, NotFoundError, RequestError
from loguru import logger

from tests.functional.testdata.data_generators import DataGenerator


@dataclass
class ElasticFaker:
    db_client: AsyncElasticsearch
    index_name: str
    path_to_index_config: str
    generator: DataGenerator
    pars_data_by_alias: bool = False

    async def create_index(self):
        if not await self.index_exists():
            schema = await self.get_index_schema()
            await self.create_index_by_schema(schema)

    async def index_exists(self) -> bool:
        return await self.db_client.indices.exists(index=self.index_name)

    async def get_index_schema(self) -> dict:
        schema = {}
        with open(self.path_to_index_config) as index_config_file:
            try:
                schema = json.load(index_config_file)
            except Exception as e:
                logger.error(e)
                raise e
        return schema

    async def create_index_by_schema(self, schema: dict):
        try:
            await self.db_client.indices.create(index=self.index_name, body=schema)
        except RequestError as e:
            if e.error != "resource_already_exists_exception":
                raise e

    async def delete_index(self):
        try:
            await self.db_client.indices.delete(index=self.index_name)
        except NotFoundError:
            pass

    async def bulk(self, data: list):
        es_data = []
        for item in data:
            es_data += [
                {"index": {"_index": self.index_name, "_id": item.id}},
                item.dict(by_alias=self.pars_data_by_alias),
            ]

        resp = await self.db_client.bulk(body=es_data)
        if resp["errors"]:
            try:
                index = resp["items"][0]["index"]["_index"]
                error = resp["items"][0]["index"]["error"]["reason"]
                logger.error(f"Elastic bulk error. Index: {index}. Error:{error}")
            except (KeyError, IndexError):
                pass
            except Exception as e:
                logger.error(f"Elastic bulk error: {e}")
                raise e
        await self.refresh_index()

    async def refresh_index(self):
        await self.db_client.indices.refresh(index=self.index_name)

    def generate_data(self):
        return self.generator.generate_data()
