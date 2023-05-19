from fastapi import Query
from pydantic import BaseModel, Field

from content.models.genre import Genre
from content.models.mixins import UUIDMixin
from content.models.person import Person


class FilmRequest(BaseModel):
    title: str = Field(
        default=Query("", alias="query[title]", description="Part of film title (for example: The Godfath)"),
    )
    description: str = Field(
        default=Query("", alias="query[description]", description="Part of film description"),
    )
    genre: str = Field(
        default=Query("", alias="query[genre]", description="The name of the genre"),
    )


class FilmResponse(UUIDMixin):
    title: str
    rating: float
    description: str
    genres: list[Genre]
    actors: list[Person]
    writers: list[Person]
    director: str = ""
