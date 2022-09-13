import pytest
from core.config import settings
from elasticsearch import AsyncElasticsearch


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(
        hosts="{es_host}:{es_port}".format(es_host=settings.ELASTIC_HOST, es_port=settings.ELASTIC_PORT)
    )
    yield client
    await client.close()
