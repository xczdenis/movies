import random
from dataclasses import dataclass
from typing import Callable, Optional

from faker import Faker
from models.film import Film
from models.genre import Genre
from models.person import Person

fake = Faker()


def fake_id():
    return fake.hexify(text="^^-^^^^-^^^^-^^^^^^^^^^")


def fake_number():
    return random.random()  # noqa: S311


def fake_title(prefix: Optional[str] = None):
    return fake.bothify(text=f"{prefix or ''}-????????? ???????-##")


async def generate_persons(items_number: int):
    return [Person(id=fake_id(), full_name=fake.name()) for _ in range(items_number)]


async def generate_genres(items_number: int):
    genres = ["drama", "comedy", "action", "sci-fi", "fantasy", "animation"]
    return [make_genre(genres) for _ in range(items_number)]


def make_genre(genres):
    genre_name = genres[random.randint(0, len(genres) - 1)]
    return Genre(id=fake_id(), name=genre_name)


async def generate_films(items_number: int):
    return [
        Film(
            id=fake_id(),
            title=fake_title("Film"),
            rating=fake_number(),
            description=fake.bothify(letters="ABCDEFGHIJKLMNOPQRSTUVW"),
            genres=await generate_genres(random.randint(1, 5)),  # noqa: S311
            actors=await generate_persons(random.randint(1, 5)),  # noqa: S311
            writers=await generate_persons(random.randint(1, 5)),  # noqa: S311
            director=fake.name(),
        )
        for _ in range(items_number)
    ]


@dataclass
class DataGenerator:
    generate_data_func: Callable
    items_number: int = 50

    async def generate_data(self):
        return await self.generate_data_func(self.items_number)
