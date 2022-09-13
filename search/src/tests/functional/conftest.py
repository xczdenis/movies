import asyncio

import pytest
from fastapi import FastAPI
from main import app as _app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return _app


pytest_plugins = (
    "tests.functional.testdata.fixtures.database",
    "tests.functional.testdata.fixtures.elastic",
    "tests.functional.testdata.fixtures.redis",
    "tests.functional.testdata.fixtures.requests",
)
