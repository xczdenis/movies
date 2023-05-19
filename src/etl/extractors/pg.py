from dataclasses import dataclass, field
from typing import Iterator

from etl.config.settings import pg_config
from etl.db_clients.pg import PGClient
from etl.extractors.base import Extractor
from etl.state import MovieStorage


@dataclass
class PostgresExtractor(Extractor):
    db_client: PGClient
    storage: MovieStorage | None = None
    batch_size: int = field(default=pg_config.POSTGRES_EXTRACTOR_BATCH_SIZE)

    def extract(self) -> Iterator[any] | None:
        pass


@dataclass
class MovieExtractor(PostgresExtractor):
    def extract(self) -> Iterator[any] | None:
        updated_at = self.storage.get_last_update_movie()
        query = self.get_query()
        cursor = self.db_client.execute(query, (updated_at,))
        while batch := cursor.fetchmany(self.batch_size):
            yield batch

    def get_query(self) -> str:
        query_template = """
            SELECT
                   fw.id,
                   fw.title,
                   fw.description,
                   fw.rating,
                   fw.type,
                   fw.created_at,
                   fw.updated_at,
                   COALESCE (
                       json_agg(
                           DISTINCT jsonb_build_object(
                               'role', pfw.role,
                               'id', p.id,
                               'full_name', p.full_name
                           )
                       ) FILTER (WHERE p.id is not null),
                       '[]'
                   ) as persons,
                   COALESCE (
                       json_agg(
                           DISTINCT jsonb_build_object(
                               'id', g.id,
                               'name', g.name
                           )
                       ) FILTER (WHERE g.id is not null),
                       '[]'
                   ) as genres
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                {condition}
                GROUP BY fw.id
                ORDER BY fw.updated_at;
        """

        updated_at = self.storage.get_last_update_movie()
        condition = "WHERE fw.updated_at > %s" if updated_at else ""
        return query_template.format(condition=condition)


@dataclass
class GenreExtractor(PostgresExtractor):
    def extract(self) -> Iterator[any] | None:
        updated_at = self.storage.get_last_update_movie()
        query = self.get_query()
        cursor = self.db_client.execute(query, (updated_at,))
        while batch := cursor.fetchmany(self.batch_size):
            yield batch

    def get_query(self) -> str:
        query_template = """
                SELECT
                   genre.id,
                   genre.name,
                   genre.created_at,
                   genre.updated_at
                FROM content.genre genre
                {condition}
                ORDER BY genre.updated_at;"""

        updated_at = self.storage.get_last_update_genres()
        condition = "WHERE genre.updated_at > %s" if updated_at else ""
        return query_template.format(condition=condition)


@dataclass
class PersonExtractor(PostgresExtractor):
    def extract(self) -> Iterator[any] | None:
        updated_at = self.storage.get_last_update_movie()
        query = self.get_query()

        cursor = self.db_client.execute(query, (updated_at,))
        while batch := cursor.fetchmany(self.batch_size):
            yield batch

    def get_query(self) -> str:
        query_template = """
                SELECT
                   person.id,
                   person.full_name,
                   person.created_at,
                   person.updated_at
                FROM content.person person
                {condition}
                ORDER BY person.updated_at;"""

        updated_at = self.storage.get_last_update_persons()
        condition = "WHERE person.updated_at > %s" if updated_at else ""
        return query_template.format(condition=condition)
