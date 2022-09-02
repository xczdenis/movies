import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass

from clients.interface import IClient


@dataclass
class SQLiteClient(IClient):
    db_path: str

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.close()
