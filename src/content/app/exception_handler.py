from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from content.exceptions import InternalNetworkConnectionError, ValidationDataError
from content.responses import ErrorResponseContent
from content.utils import get_all_sub_apps


def register_handlers(app: FastAPI):
    @app.exception_handler(ValidationDataError)
    async def validation_data_handler(request: Request, exc: ValidationDataError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=ErrorResponseContent(error=str(exc)).dict(),
        )

    @app.exception_handler(InternalNetworkConnectionError)
    async def internal_network_connection_error_handler(
        request: Request, exc: InternalNetworkConnectionError
    ):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=ErrorResponseContent(
                error="Unfortunately, the request cannot be processed "
                "because an error has occurred on our server"
            ).dict(),
        )


def register_exception_handlers(app: FastAPI):
    sub_apps = get_all_sub_apps(app)
    for _app in app, *sub_apps:
        register_handlers(_app)
