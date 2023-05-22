from http import HTTPStatus

import pytest

from content.api.v1.routes.persons import NAMESPACE
from tests.functional.utils import URLMaker

url_maker = URLMaker(namespace=NAMESPACE)


@pytest.mark.asyncio
class TestPersonDetail:
    @pytest.fixture(autouse=True)
    def setup_method(self, test_client, existing_person):
        self.test_client = test_client
        self.existing_person = existing_person

    async def test_should_return_person_info(self):
        url = url_maker.make_url("detail", person_id=self.existing_person.pk)
        expected_status_code = HTTPStatus.OK

        response = self.test_client.get(url)
        actual_status_code = response.status_code

        assert actual_status_code == expected_status_code
        assert response.body["id"] == self.existing_person.pk
        assert response.body["full_name"] == self.existing_person.full_name

    async def test_should_return_404(self):
        url = url_maker.make_url("detail", person_id="i-am-shore-that-such-id-does-not-exist")
        expected_status_code = HTTPStatus.NOT_FOUND

        response = self.test_client.get(url)
        actual_status_code = response.status_code

        assert actual_status_code == expected_status_code
