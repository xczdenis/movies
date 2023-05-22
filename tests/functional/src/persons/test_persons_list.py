import random
from http import HTTPStatus

import pytest

from content.api.v1.routes.persons import NAMESPACE
from content.core.config import settings
from tests.functional.constants import PAGINATED_RESPONSE_STRUCTURE
from tests.functional.utils import URLMaker

url_maker = URLMaker(namespace=NAMESPACE)


@pytest.mark.asyncio
class TestPersonList:
    @pytest.fixture(autouse=True)
    def setup_method(self, test_client, existing_person):
        self.test_client = test_client
        self.existing_person = existing_person

    async def test_response_status_should_be_ok(self):
        url = url_maker.make_url("list")

        response = self.test_client.get(url)

        assert response.status_code == HTTPStatus.OK

    async def test_response_body_should_be_paginated(self):
        url = url_maker.make_url("list")

        response = self.test_client.get(url)

        # response body should contain all fields from PAGINATED_RESPONSE_STRUCTURE
        for field in PAGINATED_RESPONSE_STRUCTURE:
            assert field in response.body

    @pytest.mark.parametrize(
        "page_size",
        (
            random.randint(1, settings.TESTS_MAX_PERSONS_NUMBER),
            random.randint(1, settings.TESTS_MAX_PERSONS_NUMBER),
            random.randint(1, settings.TESTS_MAX_PERSONS_NUMBER),
        ),
    )
    async def test_len_results_should_be_equal_page_size(self, page_size):
        url = url_maker.make_url("list")

        response = self.test_client.get(url, params={"page[size]": page_size})

        assert len(response.body.get("results", [])) == page_size

    async def test_search_existing_person(self, existing_person):
        url = url_maker.make_url("list")

        response = self.test_client.get(url, params={"query": existing_person.full_name})

        assert response.status_code == HTTPStatus.OK
        assert response.body["results"][0]["id"] == existing_person.pk
