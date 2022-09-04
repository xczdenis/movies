import os

from clients.pg import PGClient
from clients.sqlite import SQLiteClient
from config import BASE_DIR, config
from decorators import backoff
from processes.processes import SQLiteToPostgresProcess

sqlite_client = SQLiteClient(os.path.join(BASE_DIR, "files/db.sqlite"))
pg_client = PGClient(
    "postgres://{user}:{pwd}@{host}:{port}/{db_name}".format(
        user=config.POSTGRES_USER,
        pwd=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        db_name=config.POSTGRES_DB,
    )
)


@backoff()
def load_data():
    with pg_client.connect() as pg_connection:
        with sqlite_client.connect() as sqlite_connection:
            process = SQLiteToPostgresProcess(
                sqlite_connection=sqlite_connection, pg_connection=pg_connection
            )
            process.start()


if __name__ == "__main__":
    load_data()
