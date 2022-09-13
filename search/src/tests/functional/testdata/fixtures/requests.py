from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest
from core.config import settings
from multidict import CIMultiDictProxy

SERVICE_URL = "http://{app_host}:{app_port}".format(
    app_host=settings.SEARCH_APP_HOST, app_port=settings.SEARCH_APP_PORT
)


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession(
        headers={"Accept": "application/json", "Content-Type": "application/json"}
    )
    yield session
    await session.close()


@dataclass
class HTTPResponse:
    body: dict | list
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.get(SERVICE_URL + url, params=params) as response:
            return HTTPResponse(
                body=await response.json() if response.ok else {},
                headers=response.headers,
                status=response.status,
            )

    return inner
