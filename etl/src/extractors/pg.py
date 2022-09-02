# from dataclasses import dataclass, field
# from typing import Iterator, Optional
#
# from extractors.interface import IExtractor
# from pg_to_es.settings import settings
# from pg_to_es.state import MovieStorage
# from psycopg2.extensions import connection
#
#
# @dataclass
# class PostgresExtractor(IExtractor):
#     connection: connection
#     storage: Optional[MovieStorage]
#     batch_size: int = field(default=settings.PG_EXTRACTOR_BATCH_SIZE)
#
#     def extract(self) -> Iterator[any]:
#         pass
#
#
# @dataclass
# class MovieExtractor(PostgresExtractor):
#     def extract(self) -> Iterator[any]:
#         updated_at = self.storage.get_last_update_movie()
#         condition = "WHERE fw.updated_at > %s" if updated_at else ""
#         query = """
#         SELECT
#            fw.id,
#            fw.title,
#            fw.description,
#            fw.rating,
#            fw.type,
#            fw.created_at,
#            fw.updated_at,
#            COALESCE (
#                json_agg(
#                    DISTINCT jsonb_build_object(
#                        'person_role', pfw.role,
#                        'person_id', p.id,
#                        'person_name', p.full_name
#                    )
#                ) FILTER (WHERE p.id is not null),
#                '[]'
#            ) as persons,
#            array_agg(DISTINCT g.name) as genres
#         FROM content.film_work fw
#         LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
#         LEFT JOIN content.person p ON p.id = pfw.person_id
#         LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
#         LEFT JOIN content.genre g ON g.id = gfw.genre_id
#         {condition}
#         GROUP BY fw.id
#         ORDER BY fw.updated_at;""".format(
#             condition=condition
#         )
#
#         with self.connection.cursor() as cursor:
#             cursor.execute(query, (updated_at,))
#             while batch := cursor.fetchmany(self.batch_size):
#                 yield batch
#
#
# @dataclass
# class GenreExtractor(PostgresExtractor):
#     def extract(self) -> Iterator[any]:
#         updated_at = self.storage.get_last_update_genres()
#         condition = "WHERE genre.updated_at > %s" if updated_at else ""
#         query = """
#                 SELECT
#                    genre.id,
#                    genre.name,
#                    genre.created_at,
#                    genre.updated_at
#                 FROM content.genre genre
#                 {condition}
#                 ORDER BY genre.updated_at;""".format(
#             condition=condition
#         )
#
#         with self.connection.cursor() as cursor:
#             cursor.execute(query, (updated_at,))
#             while batch := cursor.fetchmany(self.batch_size):
#                 yield batch
#
#
# @dataclass
# class PersonExtractor(PostgresExtractor):
#     def extract(self) -> Iterator[any]:
#         updated_at = self.storage.get_last_update_persons()
#         condition = "WHERE person.updated_at > %s" if updated_at else ""
#         query = """
#                 SELECT
#                    person.id,
#                    person.full_name,
#                    person.created_at,
#                    person.updated_at
#                 FROM content.person person
#                 {condition}
#                 ORDER BY person.updated_at;""".format(
#             condition=condition
#         )
#
#         with self.connection.cursor() as cursor:
#             cursor.execute(query, (updated_at,))
#             while batch := cursor.fetchmany(self.batch_size):
#                 yield batch
