from dataclasses import dataclass

from loguru import logger
from psycopg2.extras import execute_values

from etl.db_clients.pg import PGClient
from etl.loaders.base import Loader


@dataclass
class PGLoader(Loader):
    db_client: PGClient
    scheme: str
    model: any
    table: str
    page_size: int = 100

    def load(self, data, **kwargs) -> bool:
        success = True
        query = self.get_query()
        try:
            execute_values(self.cursor, query, data, page_size=self.page_size)
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

    def get_query(self):
        fields = ",".join(self.model.__dataclass_fields__.keys())
        query_template = "INSERT INTO {scheme}.{table} ({fields}) values %s ON CONFLICT (id) DO NOTHING"
        return query_template.format(scheme=self.scheme, table=self.table, fields=fields)

    @property
    def cursor(self):
        return self.db_client.get_cursor()
