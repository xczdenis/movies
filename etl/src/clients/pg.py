from contextlib import contextmanager
from dataclasses import dataclass

import psycopg2
from clients.interface import IClient
from psycopg2.extras import RealDictCursor


@dataclass
class PGClient(IClient):
    dsn: str

    @contextmanager
    def connect(self):
        conn = psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
        conn.autocommit = True
        yield conn
        conn.close()
