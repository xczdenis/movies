import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


pytest_plugins = (
    "tests.functional.testdata.fixtures.test_client",
    "tests.functional.testdata.fixtures.fake_db",
    "tests.functional.testdata.fixtures.db_clients.elastic",
)
