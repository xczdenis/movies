import os

import pytest
from core.config import BASE_DIR, settings
from models.film import Film
from models.genre import Genre
from models.person import Person
from tests.functional.testdata.data_generators import (
    DataGenerator,
    generate_films,
    generate_genres,
    generate_persons,
)
from tests.functional.testdata.fakers import ElasticFaker


@pytest.fixture(scope="session")
async def fake_db(es_client, redis_client):
    path_to_indexes_schemas = os.path.join(BASE_DIR, "tests/functional/testdata/es_indexes_schemas")

    film_faker = ElasticFaker(
        client=es_client,
        index_name=Film.get_index_name(),
        index_path=f"{path_to_indexes_schemas}/movies.json",
        generator=DataGenerator(
            generate_data_func=generate_films, items_number=settings.TESTS_MAX_FILMS_NUMBER
        ),
    )

    person_faker = ElasticFaker(
        client=es_client,
        index_name=Person.get_index_name(),
        index_path=f"{path_to_indexes_schemas}/persons.json",
        generator=DataGenerator(
            generate_data_func=generate_persons, items_number=settings.TESTS_MAX_PERSONS_NUMBER
        ),
    )

    genre_faker = ElasticFaker(
        client=es_client,
        index_name=Genre.get_index_name(),
        index_path=f"{path_to_indexes_schemas}/genres.json",
        generator=DataGenerator(
            generate_data_func=generate_genres, items_number=settings.TESTS_MAX_GENRES_NUMBER
        ),
    )

    fake_data_set = {}

    for faker in (film_faker, person_faker, genre_faker):
        await faker.create_index()
        data = await faker.generate_data()
        await faker.bulk(data)
        fake_data_set[faker.index_name] = data

    yield fake_data_set

    for faker in (film_faker, person_faker, genre_faker):
        await faker.delete_index()
