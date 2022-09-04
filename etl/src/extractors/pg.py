from dataclasses import dataclass, field
from typing import Iterator, Optional

from config import config
from extractors.interface import IExtractor
from loguru import logger
from psycopg2.extensions import connection
from state import MovieStorage


@dataclass
class PostgresExtractor(IExtractor):
    connection: connection
    storage: Optional[MovieStorage]
    batch_size: int = field(default=config.POSTGRES_EXTRACTOR_BATCH_SIZE)

    def extract(self) -> Optional[Iterator[any]]:
        pass


@dataclass
class MovieExtractor(PostgresExtractor):
    def extract(self) -> Optional[Iterator[any]]:
        updated_at = self.storage.get_last_update_movie()
        condition = "WHERE fw.updated_at > %s" if updated_at else ""
        query = """
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
        ORDER BY fw.updated_at;""".format(
            condition=condition
        )

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, (updated_at,))
            except Exception as e:
                logger.error("Unable to fetch movies from postgres: {e}".format(e=e))
            else:
                while batch := cursor.fetchmany(self.batch_size):
                    yield batch


@dataclass
class GenreExtractor(PostgresExtractor):
    def extract(self) -> Optional[Iterator[any]]:
        updated_at = self.storage.get_last_update_genres()
        condition = "WHERE genre.updated_at > %s" if updated_at else ""
        query = """
                SELECT
                   genre.id,
                   genre.name,
                   genre.created_at,
                   genre.updated_at
                FROM content.genre genre
                {condition}
                ORDER BY genre.updated_at;""".format(
            condition=condition
        )

        with self.connection.cursor() as cursor:
            cursor.execute(query, (updated_at,))
            while batch := cursor.fetchmany(self.batch_size):
                yield batch

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, (updated_at,))
            except Exception as e:
                logger.error("Unable to fetch genres from postgres: {e}".format(e=e))
            else:
                while batch := cursor.fetchmany(self.batch_size):
                    yield batch


@dataclass
class PersonExtractor(PostgresExtractor):
    def extract(self) -> Optional[Iterator[any]]:
        updated_at = self.storage.get_last_update_persons()
        condition = "WHERE person.updated_at > %s" if updated_at else ""
        query = """
                SELECT
                   person.id,
                   person.full_name,
                   person.created_at,
                   person.updated_at
                FROM content.person person
                {condition}
                ORDER BY person.updated_at;""".format(
            condition=condition
        )

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, (updated_at,))
            except Exception as e:
                logger.error("Unable to fetch persons from postgres: {e}".format(e=e))
            else:
                while batch := cursor.fetchmany(self.batch_size):
                    yield batch
