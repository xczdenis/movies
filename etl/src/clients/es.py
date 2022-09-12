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
        if conn.ping():
            logger.info(f"Elasticsearch database connection successfully established ({self.dsn})")
        yield conn
        conn.close()
        ESClient.close_connection(connection=conn)

    @staticmethod
    def close_connection(connection: Elasticsearch):
        try:
            connection.close()
        except Exception as e:
            logger.error("Unable to close elasticsearch connection: {e}".format(e=e))
        else:
            logger.info("Elasticsearch database connection closed")
