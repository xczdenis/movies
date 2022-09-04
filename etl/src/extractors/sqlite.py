from dataclasses import dataclass, field
from sqlite3 import Connection
from typing import Iterator, Optional

from config import config
from extractors.interface import IExtractor
from loguru import logger


@dataclass
class SQLiteExtractor(IExtractor):
    connection: Connection
    table: str
    batch_size: int = field(default=config.SQLITE_EXTRACTOR_BATCH_SIZE)

    def extract(self) -> Optional[Iterator[any]]:
        cursor = self.connection.cursor()

        try:
            cursor.execute("SELECT * FROM {table}".format(table=self.table))
        except Exception as e:
            logger.error(
                "Unable to fetch data from SQLite table '{table}': {e}".format(table=self.table, e=e)
            )
        else:
            while batch := cursor.fetchmany(self.batch_size):
                yield batch
