from dataclasses import dataclass

import backoff
from elasticsearch import Elasticsearch
from loguru import logger

from etl.db_clients.base import DatabaseClient


@dataclass(slots=True)
class ESClient(DatabaseClient):
    db_type = "Elastic"
    host: str
    port: int
    user: str
    password: str
    native_client: Elasticsearch | None = None

    @property
    def hostname(self) -> str | None:
        return "{}:{}".format(self.host, self.port)

    def connect(self):
        logger.info("Connect to db: %s" % self)
        self.define_native_client()
        self.wait_until_healthy()
        logger.success("Connection to db: '%s' successfully established" % self)

    def define_native_client(self):
        self.native_client = self.create_native_client()

    def create_native_client(self) -> Elasticsearch:
        return Elasticsearch(
            "http://{host}:{port}".format(host=self.host, port=self.port),
            basic_auth=(self.user, self.password),
        )

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10)
    def wait_until_healthy(self):
        logger.debug("Waiting for Elasticsearch to become healthy on host %s" % self.hostname)
        if not self.is_healthy():
            raise ConnectionError("Elasticsearch is not healthy")

    def is_healthy(self) -> bool:
        return self.native_client.ping()

    def close(self, **kwargs):
        try:
            self.native_client.close()
        except Exception as e:
            logger.error("Unable to close connection to db '%s': %s" % (self, e))
        else:
            logger.info("Connection to db: '%s' successfully closed" % self)

    def execute(self, query: str, *args, **kwargs):
        ...
