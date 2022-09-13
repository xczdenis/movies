from http import HTTPStatus
from typing import Union, get_args, get_origin

import pytest
from api.v1.genres import Genre as GenreAPI
from models.genre import Genre
from services.utils import make_key_from_args
from tests.functional.constants import PAGINATED_RESPONSE_STRUCTURE

NAMESPACE = "genres"


@pytest.mark.asyncio
async def test_genre_detail(app, fake_db, make_get_request):
    genre = fake_db[Genre.get_index_name()][0]
    url = app.url_path_for(f"{NAMESPACE}:detail", genre_id=genre.pk)
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert response.body["id"] == genre.pk
    assert response.body["name"] == genre.name


@pytest.mark.asyncio
async def test_structure_paginated_response(app, fake_db, make_get_request):
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


@pytest.mark.parametrize("page_size", (1, 11, 21))
@pytest.mark.asyncio
async def test_genre_list(page_size, app, fake_db, make_get_request):
    url = app.url_path_for(f"{NAMESPACE}:list")
    response = await make_get_request(url, params={"page[size]": page_size})

    assert response.status == HTTPStatus.OK
    assert len(response.body.get("results", [])) == page_size


@pytest.mark.asyncio
async def test_genre_cache(app, fake_db, make_get_request, redis_client):
    genre = fake_db[Genre.get_index_name()][0]
    url = app.url_path_for(f"{NAMESPACE}:detail", genre_id=genre.pk)

    response = await make_get_request(url)

    cache_key = await make_key_from_args(model=Genre, object_id=genre.pk, _solt="detail")
    from_cache = await redis_client.get(cache_key)

    genre_from_db = GenreAPI.parse_raw(genre.json())
    genre_from_cache = GenreAPI.parse_raw(from_cache)

    assert response.status == HTTPStatus.OK
    assert genre_from_db == genre_from_cache
