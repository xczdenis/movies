from dataclasses import dataclass, field
from sqlite3 import Connection
from typing import Iterator

from config import config
from extractors.interface import IExtractor


@dataclass
class SQLiteExtractor(IExtractor):
    connection: Connection
    table: str
    batch_size: int = field(default=config.SQLITE_EXTRACTOR_BATCH_SIZE)

    def extract(self) -> Iterator[any]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM {table}".format(table=self.table))
        while batch := cursor.fetchmany(self.batch_size):
            yield batch
