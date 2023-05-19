from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from content.api.params import PaginateModel
from content.api.utils import get_rout_name
from content.api.v1.schemas.genres import GenreResponse
from content.db.shared import Filter
from content.pagination import Page, paginate
from content.services.genre import GenreService, get_genre_service

NAMESPACE = "genres"

router = APIRouter(prefix=f"/{NAMESPACE}", tags=["Genres"])


@router.get("/", name=get_rout_name(NAMESPACE, "list"), response_model=Page[GenreResponse])
async def genres_list(
    pagination: PaginateModel = Depends(),
    query: str = Query(None, description="The name of the genre to get"),
    service: GenreService = Depends(get_genre_service),
) -> Page[GenreResponse]:
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
        results=[GenreResponse.parse_obj(genre.dict()) for genre in genres],
    )


@router.get("/{genre_id}/", name=get_rout_name(NAMESPACE, "detail"), response_model=GenreResponse)
async def genre_detail(
    genre_id: str = Path(description="The ID of the genre to get"),
    service: GenreService = Depends(get_genre_service),
) -> GenreResponse:
    """
    Returns the dict with all information about the genre by ID.
    """
    genre = await service.get(object_id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    return GenreResponse(**genre.dict())
