from contextlib import contextmanager
from dataclasses import dataclass

from clients.interface import IClient
from elasticsearch import Elasticsearch


@dataclass
class ESClient(IClient):
    dsn: str

    @contextmanager
    def connect(self):
        conn = Elasticsearch(self.dsn)
        yield conn
        conn.close()
