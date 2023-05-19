from copy import copy
from http import HTTPStatus
from typing import Union, get_args, get_origin

import pytest
from api.v1.films import Film as FilmAPI
from core.config import settings
from models.film import Film
from services.utils import make_key_from_args
from tests.functional.constants import PAGINATED_RESPONSE_STRUCTURE

NAMESPACE = "films"


@pytest.mark.asyncio
async def test_film_detail(app, fake_db, make_get_request):
    film = fake_db[Film.get_index_name()][0]
    url = app.url_path_for(f"{NAMESPACE}:detail", film_id=film.pk)
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert response.body["title"] == film.title
    assert response.body["rating"] == film.rating
    assert response.body["description"] == film.description
    assert len(response.body["actors"]) == len(film.actors)
    assert len(response.body["writers"]) == len(film.writers)


@pytest.mark.asyncio
class TestFilmList:
    async def test_structure_paginated_response(self, app, fake_db, make_get_request):
        url = app.url_path_for(f"{NAMESPACE}:list")
        response = await make_get_request(url)

        no_such_field = "NO_SUCH_FIELD"

        assert response.status == HTTPStatus.OK
        assert type(response.body) == dict

        # test response fields
        for field, field_type in PAGINATED_RESPONSE_STRUCTURE.items():
            r_field = None if response.body.get(field, no_such_field) == no_such_field else field
            assert field == r_field

        # test response fields types
        for field, field_type in PAGINATED_RESPONSE_STRUCTURE.items():
            r_value = response.body.get(field)
            if get_origin(field_type) is Union:
                assert isinstance(r_value, get_args(field_type))
            else:
                assert isinstance(r_value, field_type)

    @pytest.mark.parametrize(
        "page_size",
        (
            1,
            11,
            21,
        ),
    )
    async def test_page_size(self, page_size, app, fake_db, make_get_request):
        url = app.url_path_for(f"{NAMESPACE}:list")
        response = await make_get_request(url, params={"page[size]": page_size})

        assert response.status == HTTPStatus.OK
        assert len(response.body.get("results", [])) == page_size

    @pytest.mark.parametrize("direction", ("asc", "desc"))
    async def test_sort(self, direction, app, fake_db, make_get_request):
        url = app.url_path_for(f"{NAMESPACE}:list")
        response = await make_get_request(url, params={"sort": f"rating:{direction}"})

        actual = [item["rating"] for item in response.body.get("results")]
        expected = copy(actual)
        expected.sort(reverse=direction == "desc")

        assert response.status == HTTPStatus.OK
        assert actual == expected

    async def test_search(self, app, fake_db, make_get_request):
        film = fake_db[Film.get_index_name()][0]
        pk = film.pk
        title = film.title

        url = app.url_path_for(f"{NAMESPACE}:list")
        response = await make_get_request(
            url, params={"query[title]": title, "page[size]": settings.TESTS_MAX_FILMS_NUMBER}
        )
        ids = [item["id"] for item in response.body.get("results")]

        assert response.status == HTTPStatus.OK
        assert pk in ids


@pytest.mark.asyncio
class TestFilmCache:
    async def test_cache_detail(self, app, fake_db, make_get_request, redis_client):
        film = fake_db[Film.get_index_name()][0]
        url = app.url_path_for(f"{NAMESPACE}:detail", film_id=film.pk)

        response = await make_get_request(url)

        cache_key = await make_key_from_args(model=Film, object_id=film.pk, _solt="detail")
        from_cache = await redis_client.get(cache_key)

        movie_from_db = FilmAPI.parse_raw(film.json())
        movie_from_cache = FilmAPI.parse_raw(from_cache)

        assert response.status == HTTPStatus.OK
        assert movie_from_db == movie_from_cache
