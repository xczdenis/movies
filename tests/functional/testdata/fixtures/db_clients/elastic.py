import pytest
from elasticsearch import AsyncElasticsearch

from content.core.config import settings


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(
        "http://{host}:{port}".format(host=settings.ELASTIC_HOST, port=settings.ELASTIC_PORT),
        basic_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD),
    )

    try:
        yield client
    finally:
        await client.close()
