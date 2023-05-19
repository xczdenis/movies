import json
from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch, NotFoundError, RequestError
from loguru import logger
from tests.functional.testdata.data_generators import DataGenerator


@dataclass
class ElasticFaker:
    client: AsyncElasticsearch
    index_name: str
    index_path: str
    generator: DataGenerator
    pars_data_by_alias: bool = False

    async def create_index(self):
        if not await self.client.indices.exists(index=self.index_name):
            with open(self.index_path) as f:
                try:
                    schema = json.load(f)
                except Exception as e:
                    logger.error(e)
                    raise e
                try:
                    await self.client.indices.create(index=self.index_name, body=schema)
                except RequestError as e:
                    if e.error != "resource_already_exists_exception":
                        raise e

    async def delete_index(self):
        try:
            await self.client.indices.delete(index=self.index_name)
        except NotFoundError:
            pass

    async def bulk(self, data: list):
        es_data = []
        for item in data:
            es_data += [
                {"index": {"_index": self.index_name, "_id": item.id}},
                item.dict(by_alias=self.pars_data_by_alias),
            ]

        resp = await self.client.bulk(body=es_data)
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
        await self.client.indices.refresh(index=self.index_name)

    async def generate_data(self):
        return await self.generator.generate_data()
