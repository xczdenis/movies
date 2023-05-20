from etl.config.settings import pg_config, sqlite_config
from psycopg2.extras import RealDictCursor
from etl.db_clients.context_managers import DatabaseClientContextManager

from etl.db_clients.pg import PGClient

from etl.db_clients.sqlite import SQLiteClient
from etl.processes import SQLiteToPostgres

sqlite_client: SQLiteClient = SQLiteClient.from_url("sqlite://{db}".format(db=sqlite_config.DATABASE_PATH))
pg_client: PGClient = PGClient.from_url(
    "postgres://{user}:{pwd}@{host}:{port}/{database}".format(
        user=pg_config.POSTGRES_USER,
        pwd=pg_config.POSTGRES_PASSWORD,
        host=pg_config.POSTGRES_HOST,
        port=pg_config.POSTGRES_PORT,
        database=pg_config.POSTGRES_DB,
    ),
    config={"cursor_factory": RealDictCursor},
)


def load_data():
    with DatabaseClientContextManager(db_client=sqlite_client) as db_sqlite:
        with DatabaseClientContextManager(db_client=pg_client) as db_pg:
            process = SQLiteToPostgres(sqlite_client=db_sqlite, pg_client=db_pg)
            process.run()


if __name__ == "__main__":
    load_data()
