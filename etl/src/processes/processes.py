from dataclasses import dataclass

from clients.interface import IClient
from config import config
from extractors.sqlite import SQLiteExtractor
from loaders.pg import PGLoader
from processes.interface import IProcess
from processor import ETLProcessor, Pipeline
from transformers.pg import PGTransformer


@dataclass
class SQLiteToPostgresProcess(IProcess):
    sqlite_client: IClient
    pg_client: IClient
    repeat_interval: int = 0

    def start(self):
        with self.pg_client.connect() as pg_connection:
            with self.sqlite_client.connect() as sqlite_connection:
                pipelines = []
                for table, model in config.TABLES_MAPPING.items():
                    pipelines.append(
                        Pipeline(
                            extractor=SQLiteExtractor(connection=sqlite_connection, table=table),
                            transformer=PGTransformer(model=model),
                            loader=PGLoader(
                                connection=pg_connection,
                                scheme=config.POSTGRES_SCHEME,
                                model=model,
                                table=table,
                            ),
                        )
                    )

                processor = ETLProcessor(pipelines=pipelines)

                processor.start(self.repeat_interval)
