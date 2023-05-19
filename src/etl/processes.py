from dataclasses import dataclass

from loguru import logger

from etl.base import ETL, Pipeline, run_pipelines
from etl.config import constants
from etl.config.settings import base_config, pg_config
from etl.db_clients.es import ESClient
from etl.db_clients.pg import PGClient
from etl.db_clients.sqlite import SQLiteClient
from etl.extractors.pg import GenreExtractor, MovieExtractor, PersonExtractor
from etl.extractors.sqlite import SQLiteExtractor
from etl.loaders.es import ElasticsearchLoader
from etl.loaders.pg import PGLoader
from etl.state import MovieStorage
from etl.transformers.es.genre import GenreTransformer
from etl.transformers.es.movie import MovieTransformer
from etl.transformers.es.person import PersonTransformer
from etl.transformers.pg import PGTransformer


@dataclass
class SQLiteToPostgres(ETL):
    sqlite_client: SQLiteClient
    pg_client: PGClient

    def run(self):
        logger.info("Start ETL from SQLite to PostgreSQL")
        pipelines = self.get_pipelines()
        run_pipelines(pipelines)
        logger.success("ETL from SQLite to PostgreSQL successfully finished")

    def get_pipelines(self):
        return [
            self.make_pipeline(sql_table=table, pg_table=table, model=model)
            for table, model in base_config.TABLES_MAPPING.items()
        ]

    def make_pipeline(self, sql_table: str, pg_table: str, model: dataclass):
        return Pipeline(
            extractor=SQLiteExtractor(db_client=self.sqlite_client, table=sql_table),
            transformer=PGTransformer(model=model),
            loader=PGLoader(
                db_client=self.pg_client,
                scheme=pg_config.POSTGRES_SCHEME,
                model=model,
                table=pg_table,
            ),
        )


@dataclass
class PGToESProcess(ETL):
    es_client: ESClient
    pg_client: PGClient
    storage: MovieStorage = MovieStorage()

    def run(self):
        logger.info("Starting ETL process from PostgreSQL to Elasticsearch.")

        pipelines_mapping = self.create_pipelines_mapping()

        indices = list(pipelines_mapping.keys())
        pipelines = list(pipelines_mapping.values())

        if self.indices_are_exists(indices):
            run_pipelines(pipelines)
            logger.success("ETL from PostgreSQL to Elasticsearch successfully finished")
        else:
            logger.error(
                "All or some of the required indexes were not found in the elasticsearch database. "
                "Data upload aborted."
            )

    def create_pipelines_mapping(self) -> dict[str, Pipeline]:
        es_loader = ElasticsearchLoader(db_client=self.es_client)

        return {
            constants.INDEX_MOVIES: Pipeline(
                extractor=MovieExtractor(db_client=self.pg_client, storage=self.storage),
                transformer=MovieTransformer(index_name=constants.INDEX_MOVIES),
                loader=es_loader,
                post_load_handler=self.storage.set_last_update_movie,
            ),
            constants.INDEX_GENRES: Pipeline(
                extractor=GenreExtractor(db_client=self.pg_client, storage=self.storage),
                transformer=GenreTransformer(index_name=constants.INDEX_GENRES),
                loader=es_loader,
                post_load_handler=self.storage.set_last_update_genres,
            ),
            constants.INDEX_PERSONS: Pipeline(
                extractor=PersonExtractor(db_client=self.pg_client, storage=self.storage),
                transformer=PersonTransformer(index_name=constants.INDEX_PERSONS),
                loader=es_loader,
                post_load_handler=self.storage.set_last_update_persons,
            ),
        }

    def indices_are_exists(self, indices: list[str]) -> bool:
        all_indices_are_exists = True
        for index in indices:
            if not self.es_client.native_client.indices.exists(index=index):
                all_indices_are_exists = False
                logger.error("The index '%s' doesn't exists in elasticsearch" % index)
        return all_indices_are_exists
