from dataclasses import dataclass

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from content.core.config import settings
from content.utils import case_free_pop


@dataclass(slots=True)
class AppFactory:
    @classmethod
    def make_app(cls, config: dict | None = None, router: APIRouter | None = None, **kwargs) -> FastAPI:
        title = case_free_pop(kwargs, "title", settings.PROJECT_NAME)
        _config = {k.lower(): v for k, v in config.items()}
        app = FastAPI(
            title=title,
            docs_url="/openapi",
            openapi_url="/openapi.json",
            default_response_class=ORJSONResponse,
            **_config,
            **kwargs
        )
        if router:
            app.include_router(router)
        return app
