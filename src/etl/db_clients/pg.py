from dataclasses import dataclass, field

import psycopg2
from loguru import logger
from psycopg2.extensions import connection

from etl.db_clients.base import DatabaseClient


@dataclass(slots=True)
class PGClient(DatabaseClient):
    db_type = "Postgres"
    user: str = ""
    password: str = ""
    host: str = "localhost"
    port: int = 5432
    database: str = ""
    native_client: connection | None = None
    config: dict = field(default_factory=lambda: {})

    @property
    def hostname(self) -> str | None:
        return "{}:{}".format(self.host, self.port)

    def connect(self):
        logger.info("Connect to db: %s" % self)
        self.define_native_client()
        logger.success("Connection to db: '%s' successfully established" % self)

    def define_native_client(self):
        self.native_client = self.create_native_client()

    def create_native_client(self) -> connection:
        connection_string = self.get_connection_string()
        conn = psycopg2.connect(connection_string, **self.config)
        conn.autocommit = True
        return conn

    def get_connection_string(self) -> str:
        return "postgres://{user}:{password}@{host}:{port}/{db_name}".format(
            user=self.user, password=self.password, host=self.host, port=self.port, db_name=self.database
        )

    def close(self, **kwargs):
        try:
            self.native_client.close()
        except Exception as e:
            logger.error("Unable to close postgres connection: {e}".format(e=e))
        else:
            logger.info("Connection to db: '%s' successfully closed" % self)

    def execute(self, query: str, *args, **kwargs):
        cursor = self.get_cursor()
        cursor.execute(query, *args, **kwargs)
        return cursor

    def get_cursor(self):
        return self.native_client.cursor()
