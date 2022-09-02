import os

from clients.pg import PGClient
from clients.sqlite import SQLiteClient
from config import BASE_DIR, config
from processes.processes import SQLiteToPostgresProcess

if __name__ == "__main__":
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

    process = SQLiteToPostgresProcess(sqlite_client=sqlite_client, pg_client=pg_client)
    process.start()
