import os
import random

import pytest

from content.core.config import ROOT_DIR, settings
from content.models.film import Film
from content.models.genre import Genre
from content.models.person import Person
from tests.functional.testdata.data_generators import (
    DataGenerator,
    generate_films,
    generate_genres,
    generate_persons,
)
from tests.functional.testdata.fakers import ElasticFaker


@pytest.fixture(scope="session")
async def fake_db(es_client):
    path_to_indexes_schemas = os.path.join(ROOT_DIR, "tests", "functional", "testdata", "es_indexes_schemas")

    film_faker = ElasticFaker(
        db_client=es_client,
        index_name=Film.get_index_name(),
        path_to_index_config=f"{path_to_indexes_schemas}/movies.json",
        generator=DataGenerator(
            generate_data_func=generate_films, items_number=settings.TESTS_MAX_FILMS_NUMBER
        ),
    )

    person_faker = ElasticFaker(
        db_client=es_client,
        index_name=Person.get_index_name(),
        path_to_index_config=f"{path_to_indexes_schemas}/persons.json",
        generator=DataGenerator(
            generate_data_func=generate_persons, items_number=settings.TESTS_MAX_PERSONS_NUMBER
        ),
    )

    genre_faker = ElasticFaker(
        db_client=es_client,
        index_name=Genre.get_index_name(),
        path_to_index_config=f"{path_to_indexes_schemas}/genres.json",
        generator=DataGenerator(
            generate_data_func=generate_genres, items_number=settings.TESTS_MAX_GENRES_NUMBER
        ),
    )

    fake_data_dict = {}

    for faker in (film_faker, person_faker, genre_faker):
        await faker.create_index()
        data = faker.generate_data()
        await faker.bulk(data)
        fake_data_dict[faker.index_name] = data

    yield fake_data_dict

    for faker in (film_faker, person_faker, genre_faker):
        await faker.delete_index()


@pytest.fixture(scope="function")
def existing_person(fake_db) -> Person:
    return fake_db["persons"][random.randint(0, len(fake_db["persons"]) - 1)]
