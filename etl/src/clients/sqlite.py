import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass

from clients.interface import IClient
from loguru import logger


@dataclass
class SQLiteClient(IClient):
    db_path: str

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        logger.info("SQLite database connection successfully established")
        yield conn
        conn.close()
        logger.info("SQLite database connection closed")
