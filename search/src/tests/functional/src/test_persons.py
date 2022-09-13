from http import HTTPStatus

import pytest
from models.person import Person

NAMESPACE = "persons"


@pytest.mark.asyncio
async def test_person_detail(app, fake_db, make_get_request):
    person = fake_db[Person.get_index_name()][0]
    url = app.url_path_for(f"{NAMESPACE}:detail", person_id=person.pk)
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert response.body["id"] == person.pk
    assert response.body["full_name"] == person.full_name


# @pytest.mark.asyncio
# class TestPersonList:
#     async def test_structure_paginated_response(self, app, fake_db, make_get_request):
#         url = app.url_path_for(f"{NAMESPACE}:list")
#         response = await make_get_request(url)
#
#         no_such_field = "NO_SUCH_FIELD"
#
#         assert response.status == HTTPStatus.OK
#         assert type(response.body) == dict
#
#         # test response fields
#         for field, field_type in PAGINATED_RESPONSE_STRUCTURE.items():
#             r_field = None if response.body.get(field, no_such_field) == no_such_field else field
#             assert field == r_field
#
#         # test response fields types
#         for field, field_type in PAGINATED_RESPONSE_STRUCTURE.items():
#             r_value = response.body.get(field)
#             if get_origin(field_type) is Union:
#                 assert isinstance(r_value, get_args(field_type))
#             else:
#                 assert isinstance(r_value, field_type)
#
#     @pytest.mark.parametrize(
#         "page_size",
#         (
#             random.randint(1, settings.TESTS_MAX_PERSONS_NUMBER),
#             random.randint(1, settings.TESTS_MAX_PERSONS_NUMBER),
#             random.randint(1, settings.TESTS_MAX_PERSONS_NUMBER),
#         ),
#     )
#     async def test_page_size(self, page_size, app, fake_db, make_get_request):
#         url = app.url_path_for(f"{NAMESPACE}:list")
#         response = await make_get_request(url, params={"page[size]": page_size})
#
#         assert response.status == HTTPStatus.OK
#         assert len(response.body.get("results", [])) == page_size
#
#     async def test_search(self, app, fake_db, make_get_request):
#         person = fake_db[Person.get_index_name()][0]
#         pk = person.pk
#         full_name = person.full_name
#
#         url = app.url_path_for(f"{NAMESPACE}:list")
#         response = await make_get_request(
#             url, params={"query": full_name, "page[size]": settings.TESTS_MAX_PERSONS_NUMBER}
#         )
#         ids = [item["id"] for item in response.body.get("results")]
#
#         assert response.status == HTTPStatus.OK
#         assert pk in ids
#
#
# @pytest.mark.asyncio
# async def test_person_cache(app, fake_db, make_get_request, redis_client):
#     person = fake_db[Person.get_index_name()][0]
#     url = app.url_path_for(f"{NAMESPACE}:detail", person_id=person.pk)
#
#     response = await make_get_request(url)
#
#     cache_key = await make_key_from_args(model=Person, object_id=person.pk, _solt="detail")
#     from_cache = await redis_client.get(cache_key)
#
#     genre_from_db = PersonAPI.parse_raw(person.json())
#     genre_from_cache = PersonAPI.parse_raw(from_cache)
#
#     assert response.status == HTTPStatus.OK
#     assert genre_from_db == genre_from_cache
