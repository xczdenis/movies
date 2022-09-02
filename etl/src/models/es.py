from pydantic import BaseModel, Field


class Person(BaseModel):
    id: str
    full_name: str


class Genre(BaseModel):
    id: str
    name: str


class PersonInMovie(BaseModel):
    id: str = Field(alias="person_id")
    name: str = Field(alias="person_name")


class Movie(BaseModel):
    id: str
    imdb_rating: float = Field(alias="rating")
    title: str = ""
    genre: str = ""
    description: str = ""
    director: str = ""
    actors_names: str = ""
    writers_names: str = ""
    actors: list[PersonInMovie] = []
    writers: list[PersonInMovie] = []
