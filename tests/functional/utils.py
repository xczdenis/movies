from dataclasses import dataclass

from multidict import CIMultiDictProxy
from starlette.testclient import TestClient

from content.api.utils import make_rout_name
from content.main import app


@dataclass
class HTTPResponse:
    body: dict | list
    headers: CIMultiDictProxy[str]
    status_code: int


@dataclass
class APIClient:
    test_client: TestClient

    def get(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("get", url, **kwargs)

    def post(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("post", url, **kwargs)

    def delete(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("delete", url, **kwargs)

    def put(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("put", url, **kwargs)

    def request(self, method: str, url: str, **kwargs) -> HTTPResponse:
        response = self.test_client.request(method, url, **kwargs)
        return HTTPResponse(
            body=response.json() if response.is_success else {},
            headers=response.headers,
            status_code=response.status_code,
        )


@dataclass
class URLMaker:
    namespace: str

    def make_url(self, url_name: str = "", **url_params):
        rout_name = make_rout_name(self.namespace, url_name)
        return app.url_path_for(rout_name, **url_params)
