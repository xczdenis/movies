import aioredis
import pytest
from core.config import settings


@pytest.fixture(scope="session")
async def redis_client():
    redis = await aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    await redis.flushall()
    yield redis
    await redis.close()
    await redis.connection_pool.disconnect()
