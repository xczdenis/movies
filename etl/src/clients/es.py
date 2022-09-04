from contextlib import contextmanager
from dataclasses import dataclass

from clients.interface import IClient
from elasticsearch import Elasticsearch
from loguru import logger


@dataclass
class ESClient(IClient):
    dsn: str

    @contextmanager
    def connect(self):
        conn = Elasticsearch(self.dsn)
        logger.info("Elasticsearch database connection successfully established")
        yield conn
        conn.close()
        logger.info("Elasticsearch database connection closed")
