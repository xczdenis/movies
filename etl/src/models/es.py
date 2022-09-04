from pydantic import BaseModel


class Person(BaseModel):
    id: str
    full_name: str


class Genre(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: str
    title: str
    description: str = ""
    rating: float = 0.0
    genres: list[Genre] = []
    genres_names: str = ""
    actors: list[Person] = []
    actors_names: str = ""
    writers: list[Person] = []
    writers_names: str = ""
    director: str = ""
