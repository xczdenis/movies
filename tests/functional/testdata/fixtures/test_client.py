import pytest
from fastapi.testclient import TestClient

from content.main import app
from tests.functional.utils import APIClient


@pytest.fixture(scope="session")
async def test_client():
    with TestClient(app) as fast_api_test_client:
        yield APIClient(test_client=fast_api_test_client)
        fast_api_test_client.close()
