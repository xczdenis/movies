from http import HTTPStatus

from api.params import PaginateModel, SortModel
from api.utils import get_rout_name
from db.shared import Filter, Term
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from models.genre import Genre
from models.mixins import UUIDMixin
from models.person import Person
from pagination import Page, paginate
from pydantic import BaseModel, Field
from services.film import FilmService, get_film_service

router = APIRouter()

NAMESPACE = "films"


class Film(UUIDMixin):
    title: str
    rating: float
    description: str
    genres: list[Genre]
    actors: list[Person]
    writers: list[Person]
    director: str = ""


class QueryModel(BaseModel):
    title: str = Field(
        default=Query("", alias="query[title]", description="Part of film title (for example: The Godfath"),
    )
    description: str = Field(
        default=Query("", alias="query[description]", description="Part of film description"),
    )
    genre: str = Field(
        default=Query("", alias="query[genre]", description="The name of the genre"),
    )


@router.get(
    "/",
    name=get_rout_name(NAMESPACE, "list"),
    response_model=Page[Film],
    response_description="List of films",
)
async def films_list(
    pagination: PaginateModel = Depends(),
    sort: SortModel = Depends(),
    query: QueryModel = Depends(),
    service: FilmService = Depends(get_film_service),
) -> Page[Film]:
    """
    Returns list of films by the parameters specified in the query.
    Each element of the list is a dict of the Film structure.
    """
    total_films, films = await service.all(
        page_size=pagination.page_size,
        page=pagination.page,
        sort=sort.sort,
        filter=Filter(
            lookups={"title": query.title, "description": query.description, "genres__name": query.genre},
            term=Term.AND,
        ),
    )

    return paginate(
        count=total_films,
        page_size=pagination.page_size,
        current_page=pagination.page,
        results=[Film(**film.dict()) for film in films],
    )


@router.get("/{film_id}", name=get_rout_name(NAMESPACE, "detail"), response_model=Film)
async def film_detail(
    film_id: str = Path(description="The ID of the film to get"),
    service: FilmService = Depends(get_film_service),
) -> Film:
    """
    Returns the dict with all information about the film by ID
    """
    film = await service.get(object_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return Film(**film.dict())
