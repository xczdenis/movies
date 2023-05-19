import os
import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection

from loguru import logger

from etl.db_clients.base import DatabaseClient


@dataclass(slots=True)
class SQLiteClient(DatabaseClient):
    db_type = "SQLite"
    database: str = ""
    native_client: Connection | None = None

    @property
    def hostname(self) -> str | None:
        parts_of_database = self.database.split("/")
        if len(parts_of_database) > 0:
            return parts_of_database[-1]
        return ""

    def connect(self):
        logger.info("Connect to db: %s" % self)
        self.define_native_client()
        logger.success("Connection to db: '%s' successfully established" % self)

    def define_native_client(self):
        self.native_client = self.create_native_client()

    def create_native_client(self) -> Connection:
        if self.database_exists():
            connection = sqlite3.connect(self.database)
            connection.row_factory = sqlite3.Row
            return connection

    def database_exists(self) -> bool:
        if not os.path.exists(self.database):
            raise FileNotFoundError("No such file: %s" % self.database)
        return True

    def close(self, **kwargs):
        self.native_client.close()
        logger.info("Connection to db: '%s' closed" % self)

    def execute(self, query: str, *args, **kwargs):
        cursor = self.get_cursor()
        return cursor.execute(query)

    def get_cursor(self) -> sqlite3.Cursor:
        return self.native_client.cursor()
