from fastapi import FastAPI

from content.api.v1 import router_v1
from content.app import factories
from content.core.config import settings
from content.responses import ErrorResponseContent

global_responses = {
    500: {"model": ErrorResponseContent, "description": "Internal server error"},
    400: {"model": ErrorResponseContent, "description": "Bad request"},
}


def mount_sub_app(main_app: FastAPI, api_version_prefix: str, sub_app: FastAPI):
    main_app.mount(f"/{settings.BASE_API_PREFIX}/{api_version_prefix}", sub_app)


def create_app(config: dict) -> FastAPI:
    app_factory = factories.AppFactory()

    global_app_attributes = {"responses": {**global_responses}}

    main_app = app_factory.make_app(**config, **global_app_attributes)

    app_v1 = app_factory.make_app(router=router_v1, **config, **global_app_attributes)
    # add_pagination(app_v1)

    mount_sub_app(main_app, settings.API_V1_PREFIX, app_v1)

    return main_app
