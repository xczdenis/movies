from http import HTTPStatus

from api.params import PaginateModel
from api.utils import get_rout_name
from db.shared import Filter
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from models.mixins import UUIDMixin
from pagination import Page, paginate
from services.genre import GenreService, get_genre_service

router = APIRouter()

NAMESPACE = "genres"


class Genre(UUIDMixin):
    name: str


@router.get("/", name=get_rout_name(NAMESPACE, "list"), response_model=Page[Genre])
async def genres_list(
    pagination: PaginateModel = Depends(),
    query: str = Query(None, description="The name of the genre to get"),
    service: GenreService = Depends(get_genre_service),
) -> Page[Genre]:
    """
    Returns list of genres by the parameters specified in the query.
    Each element of the list is a dict of the Genre structure.
    """
    total_genres, genres = await service.all(
        page_size=pagination.page_size,
        page=pagination.page,
        filter=Filter(lookups={"name": query}),
    )

    return paginate(
        count=total_genres,
        page_size=pagination.page_size,
        current_page=pagination.page,
        results=[Genre.parse_obj(genre.dict()) for genre in genres],
    )


@router.get("/{genre_id}", name=get_rout_name(NAMESPACE, "detail"), response_model=Genre)
async def genre_detail(
    genre_id: str = Path(description="The ID of the genre to get"),
    service: GenreService = Depends(get_genre_service),
) -> Genre:
    """
    Returns the dict with all information about the genre by ID.
    """
    genre = await service.get(object_id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    return Genre(**genre.dict())
