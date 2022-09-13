import uvicorn as uvicorn
from api.v1 import films, genres, persons
from core.config import settings
from core.logger import UVICORN_LOGGING_CONFIG, setup_logging
from db import cache, db
from db.adapters.elastic import ElasticDB
from db.adapters.redis import RedisStorage
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    cache.cache_db = RedisStorage(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    db.db = ElasticDB(host=settings.ELASTIC_HOST, port=settings.ELASTIC_PORT)


@app.on_event("shutdown")
async def shutdown():
    await cache.cache_db.close()
    await db.db.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    setup_logging(settings.LOG_LEVEL, settings.JSON_LOGS)

    uvicorn.run(
        "main:app",
        host=settings.SEARCH_APP_HOST,
        port=int(settings.SEARCH_APP_PORT),
        log_config=UVICORN_LOGGING_CONFIG,
    )
