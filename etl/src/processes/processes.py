from dataclasses import dataclass
from sqlite3 import Connection as SQLite3Connection

import const
from config import config
from elasticsearch import Elasticsearch
from extractors.pg import GenreExtractor, MovieExtractor, PersonExtractor
from extractors.sqlite import SQLiteExtractor
from loaders.es import ElasticsearchLoader
from loaders.pg import PGLoader
from loguru import logger
from processes.interface import IProcess
from processor import ETLProcessor, Pipeline
from psycopg2.extensions import connection as psycopg2_connection
from state import MovieStorage
from transformers.es.genre import GenreTransformer
from transformers.es.movie import MovieTransformer
from transformers.es.person import PersonTransformer
from transformers.pg import PGTransformer


@dataclass
class SQLiteToPostgresProcess(IProcess):
    sqlite_connection: SQLite3Connection
    pg_connection: psycopg2_connection
    repeat_interval: int = 0

    def start(self):
        pipelines = []
        for table, model in config.TABLES_MAPPING.items():
            pipelines.append(
                Pipeline(
                    extractor=SQLiteExtractor(connection=self.sqlite_connection, table=table),
                    transformer=PGTransformer(model=model),
                    loader=PGLoader(
                        connection=self.pg_connection,
                        scheme=config.POSTGRES_SCHEME,
                        model=model,
                        table=table,
                    ),
                )
            )

        processor = ETLProcessor(pipelines=pipelines)

        processor.start(self.repeat_interval)


@dataclass
class PGToESProcess(IProcess):
    es_connection: Elasticsearch
    pg_connection: psycopg2_connection
    repeat_interval: int = 0
    storage: MovieStorage = MovieStorage("state.json")

    def start(self):
        es_loader = ElasticsearchLoader(connection=self.es_connection)

        pipelines_mapping = {
            const.INDEX_MOVIES: Pipeline(
                extractor=MovieExtractor(connection=self.pg_connection, storage=self.storage),
                transformer=MovieTransformer(index_name=const.INDEX_MOVIES),
                loader=es_loader,
                post_load_handler=self.storage.set_last_update_movie,
            ),
            const.INDEX_GENRES: Pipeline(
                extractor=GenreExtractor(connection=self.pg_connection, storage=self.storage),
                transformer=GenreTransformer(index_name=const.INDEX_GENRES),
                loader=es_loader,
                post_load_handler=self.storage.set_last_update_genres,
            ),
            const.INDEX_PERSONS: Pipeline(
                extractor=PersonExtractor(connection=self.pg_connection, storage=self.storage),
                transformer=PersonTransformer(index_name=const.INDEX_PERSONS),
                loader=es_loader,
                post_load_handler=self.storage.set_last_update_persons,
            ),
        }

        all_required_indices_are_exists = True
        for required_index in pipelines_mapping.keys():
            if not self.es_connection.indices.exists(index=required_index):
                all_required_indices_are_exists = False
                logger.error(
                    "The index '{index}' doesn't exists in elasticsearch".format(index=required_index)
                )

        if all_required_indices_are_exists:
            processor = ETLProcessor(pipelines=list(pipelines_mapping.values()))
            processor.start(self.repeat_interval)
        else:
            logger.info(
                "All or some of the required indexes were not found in the elasticsearch database. "
                "Data upload aborted."
            )
