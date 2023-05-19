from psycopg2.extras import RealDictCursor

from etl.config.settings import es_config, pg_config
from etl.db_clients.context_managers import DatabaseClientContextManager
from etl.db_clients.es import ESClient
from etl.db_clients.pg import PGClient
from etl.helpers import create_es_indexes
from etl.processes import PGToESProcess

es_client: ESClient = ESClient.from_url(
    "elasticsearch://{user}:{password}@{host}:{port}".format(
        user=es_config.ELASTIC_USER,
        password=es_config.ELASTIC_PASSWORD,
        host=es_config.ELASTIC_HOST,
        port=es_config.ELASTIC_PORT,
    )
)
pg_client: PGClient = PGClient.from_url(
    "postgres://{user}:{pwd}@{host}:{port}/{db_name}".format(
        user=pg_config.POSTGRES_USER,
        pwd=pg_config.POSTGRES_PASSWORD,
        host=pg_config.POSTGRES_HOST,
        port=pg_config.POSTGRES_PORT,
        db_name=pg_config.POSTGRES_DB,
    ),
    config={"cursor_factory": RealDictCursor},
)


def load_data():
    with DatabaseClientContextManager(db_client=es_client) as db_es:
        with DatabaseClientContextManager(db_client=pg_client) as db_pg:
            create_es_indexes(db_es.native_client, es_config.ES_INDEXES)
            process = PGToESProcess(es_client=db_es, pg_client=db_pg)
            process.run()


if __name__ == "__main__":
    load_data()
