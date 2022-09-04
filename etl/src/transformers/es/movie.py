from dataclasses import dataclass
from typing import Optional

from loguru import logger
from models.es import Movie
from transformers.interface import IESTransformer


@dataclass
class MovieTransformer(IESTransformer):
    index_name: str

    ROLE_ACTOR = "actor"
    ROLE_DIRECTOR = "director"
    ROLE_WRITER = "writer"

    def transform_row(self, row_data) -> Optional[Movie]:
        row_data["genres_names"] = " ".join([genre["name"] for genre in row_data.get("genres", [])])

        MovieTransformer.__add_persons_names(row_data, "director", MovieTransformer.ROLE_DIRECTOR)
        MovieTransformer.__add_persons_names(row_data, "actors_names", MovieTransformer.ROLE_ACTOR)
        MovieTransformer.__add_persons_names(row_data, "writers_names", MovieTransformer.ROLE_WRITER)

        MovieTransformer.__add_persons(row_data, "actors", MovieTransformer.ROLE_ACTOR)
        MovieTransformer.__add_persons(row_data, "writers", MovieTransformer.ROLE_WRITER)

        try:
            return Movie.parse_obj(row_data)
        except Exception as e:
            logger.error(
                "An error occurred during movie data transformation. ID: {id}. Error: {error}".format(
                    id=row_data.get("id"), error=e
                )
            )

        return None

    @staticmethod
    def __add_persons(row_data, field: str, role: str) -> None:
        persons = MovieTransformer.__get_persons_by_role(row_data, role)
        row_data[field] = [person for person in persons]

    @staticmethod
    def __add_persons_names(row_data, field: str, role: str) -> None:
        persons = MovieTransformer.__get_persons_names_by_role(row_data, role)
        row_data[field] = " ".join(persons)

    @staticmethod
    def __get_persons_names_by_role(row_data, role: str) -> list[str]:
        persons = MovieTransformer.__get_persons_by_role(row_data, role)
        return [person.get("full_name", "") for person in persons if person.get("full_name", "") != ""]

    @staticmethod
    def __get_persons_by_role(row_data, role: str) -> list[dict]:
        persons = row_data.get("persons", [])
        return list(filter(lambda x: x.get("role") == role, persons))
