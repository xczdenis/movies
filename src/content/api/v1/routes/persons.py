from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from content.api.params import PaginateModel
from content.api.utils import make_rout_name
from content.api.v1.schemas.persons import PersonResponse
from content.db.shared import Filter, Term
from content.models.film import Film
from content.pagination import Page, paginate
from content.services.person import PersonService, get_person_service

NAMESPACE = "persons"

router = APIRouter(prefix=f"/{NAMESPACE}", tags=["Persons"])


@router.get(
    "",
    name=make_rout_name(NAMESPACE, "list"),
    response_model=Page[PersonResponse],
    response_description="List of persons",
)
async def persons_list(
    pagination: PaginateModel = Depends(),
    query: str = Query(None, description="Filter by person name"),
    service: PersonService = Depends(get_person_service),
) -> Page[PersonResponse]:
    """
    Returns list of persons by the parameters specified in the query.
    Each element of the list is a dict of the Person structure.
    """
    total_persons, persons = await service.all(
        page_size=pagination.page_size,
        page=pagination.page,
        filter=Filter(lookups={"full_name": query}),
    )

    return paginate(
        count=total_persons,
        page_size=pagination.page_size,
        current_page=pagination.page,
        results=[PersonResponse(**person.dict()) for person in persons],
    )


@router.get("/{person_id}/", name=make_rout_name(NAMESPACE, "detail"), response_model=PersonResponse)
async def person_detail(
    person_id: str = Path(description="The ID of the person to get"),
    service: PersonService = Depends(get_person_service),
) -> PersonResponse:
    """
    Returns the dict with all information about the person by ID.
    """
    person = await service.get(object_id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person not found")
    return PersonResponse(**person.dict())


@router.get(
    "/{person_id}/films/", name=make_rout_name(NAMESPACE, "films_by_person"), response_model=Page[Film]
)
async def films_by_person(
    person_id: str = Path(description="The ID of the person whose films you want to get"),
    pagination: PaginateModel = Depends(),
    service: PersonService = Depends(get_person_service),
) -> Page[Film]:
    """
    Returns all films where the person fond by **person_id** is an actor or writer
    """
    total_films, films = await service.all_films_by_person(
        page_size=pagination.page_size,
        page=pagination.page,
        filter=Filter(lookups={"actors__id": person_id, "writers__id": person_id}, term=Term.OR),
    )

    return paginate(
        count=total_films,
        page_size=pagination.page_size,
        current_page=pagination.page,
        results=[Film(**film.dict()) for film in films],
    )
