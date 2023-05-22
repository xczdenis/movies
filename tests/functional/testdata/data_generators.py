import random
from dataclasses import dataclass
from typing import Callable

from faker import Faker

from content.models.film import Film
from content.models.genre import Genre
from content.models.person import Person

fake = Faker()


def fake_id():
    return fake.hexify(text="^^-^^^^-^^^^-^^^^^^^^^^")


def fake_number():
    return random.random()  # noqa: S311


def fake_title(prefix: str = ""):
    return fake.bothify(text=f"{prefix}-????????? ???????-##")


def make_person() -> Person:
    return Person(id=fake_id(), full_name=fake.name())


def make_genre() -> Genre:
    genre_name = get_random_genre_name()
    return Genre(id=fake_id(), name=genre_name)


def get_random_genre_name() -> str:
    genres = ["drama", "comedy", "action", "sci-fi", "fantasy", "animation", "horror"]
    return genres[random.randint(0, len(genres) - 1)]


def generate_persons(items_number: int = 50):
    return [make_person() for _ in range(items_number)]


def generate_genres(items_number: int = 50):
    return [make_genre() for _ in range(items_number)]


def generate_films(items_number: int):
    return [
        Film(
            id=fake_id(),
            title=fake_title("Film"),
            rating=fake_number(),
            description=fake.bothify(letters="ABCDEFGHIJKLMNOPQRSTUVW"),
            genres=generate_genres(random.randint(1, 5)),  # noqa: S311
            actors=generate_persons(random.randint(1, 5)),  # noqa: S311
            writers=generate_persons(random.randint(1, 5)),  # noqa: S311
            director=fake.name(),
        )
        for _ in range(items_number)
    ]


@dataclass
class DataGenerator:
    generate_data_func: Callable
    items_number: int = 50

    def generate_data(self):
        return self.generate_data_func(self.items_number)
