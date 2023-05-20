from dataclasses import dataclass, field
from sqlite3 import Cursor
from typing import Generator

from loguru import logger

from etl.config.settings import sqlite_config
from etl.db_clients.sqlite import SQLiteClient
from etl.extractors.base import Extractor


@dataclass
class SQLiteExtractor(Extractor):
    db_client: SQLiteClient
    table: str
    batch_size: int = field(default=sqlite_config.SQLITE_EXTRACTOR_BATCH_SIZE)

    def extract(self, *args, **kwargs) -> Generator:
        cursor = self.cursor
        try:
            # cursor.execute("SELECT * FROM {table}".format(table=self.table))
            query = "SELECT * FROM {table}"
            cursor.execute(query, (self.table,))
        except Exception as e:
            logger.error(
                "Unable to fetch data from SQLite table '{table}': {e}".format(table=self.table, e=e)
            )
        else:
            while batch := cursor.fetchmany(self.batch_size):
                yield batch

    @property
    def cursor(self) -> Cursor:
        return self.db_client.get_cursor()
