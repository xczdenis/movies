from clients.es import ESClient
from clients.pg import PGClient
from config import config
from decorators import backoff
from helpers import create_es_indexes
from processes.processes import PGToESProcess

es_client = ESClient("{host}:{port}".format(host=config.ELASTIC_HOST, port=config.ELASTIC_PORT))
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
        with es_client.connect() as es_connection:
            create_es_indexes(es_connection, config.ES_INDEXES)

            process = PGToESProcess(
                es_connection=es_connection, pg_connection=pg_connection,
                repeat_interval=config.PG_TO_ES_REPEAT_INTERVAL,
            )
            process.start()


if __name__ == '__main__':
    load_data()
