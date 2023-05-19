from fastapi import APIRouter

from content.api.v1.routes import films, genres, persons

router_v1 = APIRouter()

router_v1.include_router(films.router)
router_v1.include_router(genres.router)
router_v1.include_router(persons.router)
