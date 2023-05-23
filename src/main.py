import asyncio
import socket
from dataclasses import dataclass

from elasticsearch import AsyncElasticsearch, Elasticsearch


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
    # timeout = 20
    # print(f"sleep {timeout} sec")
    # await asyncio.sleep(timeout)
    response = await es_client.ping()
    print(f"main_http ping = {response}")

    # await person_faker.create_index()
    #
    await es_client.close()


async def main_https():
    es_client = AsyncElasticsearch(hosts=["https://elasticsearch:9200"], basic_auth=("elastic", "123qwe"))
    # person_faker = ElasticFaker(db_client=es_client, index_name="movies")
    # timeout = 20
    # print(f"sleep {timeout} sec")
    # await asyncio.sleep(timeout)
    response = await es_client.ping()
    print(f"main_https ping = {response}")

    # await person_faker.create_index()
    #
    await es_client.close()


async def main_http_sync():
    es_client = Elasticsearch(
        hosts=["http://elasticsearch:9200"], basic_auth=("elastic", "123qwe"), request_timeout=4
    )

    hostname = "elasticsearch"  # Замените на имя вашего хоста
    ip_address = socket.gethostbyname(hostname)
    print(f"IP address of {hostname} is {ip_address}")

    response = es_client.search()
    print(f"search = {response}")

    response = es_client.info()
    print(f"info = {response}")
    es_client.close()


async def main_real_ip():
    hostname = "elasticsearch"  # Замените на имя вашего хоста
    ip_address = socket.gethostbyname(hostname)
    print(f"main_real_ip IP address of {hostname} is {ip_address}")

    es_client = Elasticsearch(hosts=[f"http://{ip_address}:9200"], basic_auth=("elastic", "123qwe"))

    response = es_client.search()
    print(f"search = {response}")

    response = es_client.info()
    print(f"info = {response}")
    es_client.close()


async def main():
    await main_http()
    await main_https()
    await main_http_sync()
    await main_real_ip()


if __name__ == "__main__":
    asyncio.run(
        main(),
    )
