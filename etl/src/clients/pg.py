from contextlib import contextmanager
from dataclasses import dataclass

import psycopg2
from clients.interface import IClient
from loguru import logger
from psycopg2.extensions import connection as pg_connection
from psycopg2.extras import RealDictCursor


@dataclass
class PGClient(IClient):
    dsn: str

    @contextmanager
    def connect(self):
        conn = psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
        conn.autocommit = True
        logger.info("Postgres database connection successfully established")
        yield conn
        conn.close()
        PGClient.close_connection(connection=conn)

    @staticmethod
    def close_connection(connection: pg_connection):
        try:
            connection.close()
        except Exception as e:
            logger.error("Unable to close postgres connection: {e}".format(e=e))
        else:
            logger.info("Postgres database connection closed")
