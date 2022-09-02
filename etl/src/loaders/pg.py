from dataclasses import dataclass

from loaders.interface import ILoader
from loguru import logger
from psycopg2.extensions import connection
from psycopg2.extras import execute_values


@dataclass
class PGLoader(ILoader):
    connection: connection
    scheme: str
    model: any
    table: str
    page_size: int = 100

    def load(self, data) -> bool:
        success = True
        fields = ",".join(self.model.__dataclass_fields__.keys())
        query_template = "INSERT INTO {scheme}.{table} ({fields}) values %s ON CONFLICT (id) DO NOTHING"
        query = query_template.format(scheme=self.scheme, table=self.table, fields=fields)

        try:
            execute_values(self.connection.cursor(), query, data, page_size=self.page_size)
            logger.info(
                "The data was successfully uploaded to Postgres. "
                "Table: {scheme}.{table}. Row count: {row_count}".format(
                    scheme=self.scheme, table=self.table, row_count=len(data)
                )
            )
        except Exception as e:
            logger.error(e)
            success = False

        return success
