from fastapi import FastAPI

from content.api.dependencies import cache, db
from content.core.config import settings
from content.db.adapters.elastic import ElasticDB
from content.db.adapters.redis import RedisStorage
from content.utils import get_all_sub_apps


def register_handlers(app: FastAPI):
    @app.on_event("startup")
    async def startup_event_handler():
        cache.cache_db = RedisStorage(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        db.db = ElasticDB(host=settings.ELASTIC_HOST, port=settings.ELASTIC_PORT)

    @app.on_event("shutdown")
    async def shutdown_event_handler():
        await cache.cache_db.close()
        await db.db.close()


def register_event_handlers(app: FastAPI):
    sub_apps = get_all_sub_apps(app)
    for _app in app, *sub_apps:
        register_handlers(_app)
