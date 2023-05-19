import uvicorn

from content.app import create_app
from content.app.event_handlers import register_event_handlers
from content.app.exception_handler import register_exception_handlers
from content.core.config import settings
from content.core.logger import setup_logging

app = create_app(settings.dict())

register_event_handlers(app)
register_exception_handlers(app)

if __name__ == "__main__":
    setup_logging(settings.LOG_LEVEL, settings.JSON_LOGS)

    uvicorn.run("main:app", host=settings.CONTENT_APP_HOST, port=int(settings.CONTENT_APP_PORT))
