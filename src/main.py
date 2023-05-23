import asyncio
from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch


@dataclass
class ElasticFaker:
    db_client: AsyncElasticsearch
    index_name: str

    async def create_index(self):
        if not await self.index_exists():
            print(f"Index {self.index_name} doesn't exist")
        else:
            print(f"Index {self.index_name} exists")

    async def index_exists(self) -> bool:
        return await self.db_client.indices.exists(index=self.index_name)


async def main_http():
    es_client = AsyncElasticsearch(hosts=["http://elasticsearch:9200"], basic_auth=("elastic", "123qwe"))
    # person_faker = ElasticFaker(db_client=es_client, index_name="movies")
    timeout = 20
    print(f"sleep {timeout} sec")
    await asyncio.sleep(timeout)
    response = await es_client.ping()
    print(f"main_http ping = {response}")

    # await person_faker.create_index()
    #
    await es_client.close()


async def main_https():
    es_client = AsyncElasticsearch(hosts=["https://elasticsearch:9200"], basic_auth=("elastic", "123qwe"))
    # person_faker = ElasticFaker(db_client=es_client, index_name="movies")
    timeout = 20
    print(f"sleep {timeout} sec")
    await asyncio.sleep(timeout)
    response = await es_client.ping()
    print(f"main_https ping = {response}")

    # await person_faker.create_index()
    #
    await es_client.close()


async def main():
    await main_http()
    await main_https()


if __name__ == "__main__":
    asyncio.run(
        main(),
    )
