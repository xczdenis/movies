from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path

from content.api.params import PaginateModel, SortModel
from content.api.utils import make_rout_name
from content.api.v1.schemas.films import FilmRequest, FilmResponse
from content.db.shared import Filter, Term
from content.pagination import Page, paginate
from content.services.film import FilmService, get_film_service

NAMESPACE = "films"

router = APIRouter(prefix=f"/{NAMESPACE}", tags=["Films"])


@router.get(
    "/",
    name=make_rout_name(NAMESPACE, "list"),
    response_model=Page[FilmResponse],
    response_description="List of films",
)
async def films_list(
    pagination: PaginateModel = Depends(),
    sort: SortModel = Depends(),
    query: FilmRequest = Depends(),
    service: FilmService = Depends(get_film_service),
) -> Page[FilmResponse]:
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
        results=[FilmResponse(**film.dict()) for film in films],
    )


@router.get("/{film_id}/", name=make_rout_name(NAMESPACE, "detail"), response_model=FilmResponse)
async def film_detail(
    film_id: str = Path(description="The ID of the film to get"),
    service: FilmService = Depends(get_film_service),
) -> FilmResponse:
    """
    Returns the dict with all information about the film by ID
    """
    film = await service.get(object_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")
    return FilmResponse(**film.dict())
