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


async def main():
    es_client = AsyncElasticsearch(hosts=["http://elasticsearch:9200"], basic_auth=("elastic", "123qwe"))
    # person_faker = ElasticFaker(db_client=es_client, index_name="movies")

    response = await es_client.ping()
    print(f"ping4 = {response}")

    # await person_faker.create_index()
    #
    await es_client.close()


if __name__ == "__main__":
    asyncio.run(main())
