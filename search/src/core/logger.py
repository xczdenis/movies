import logging
import sys
from dataclasses import dataclass
from typing import Optional

from loguru import logger

# custom handlers removed, we catch logs via loguru
UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "propagate": False},
    },
}


@dataclass
class LoggerFilter:
    level: str = "DEBUG"
    exclude_levels: Optional[list[str]] = None

    def __post_init__(self):
        self.level_no = logger.level(self.level).no

    def __call__(self, record):
        record_level = record["level"]
        return record_level.no >= self.level_no and (
            not self.exclude_levels or record_level.name not in self.exclude_levels
        )


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(log_level: str, json_logs: bool):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level)

    # remove every other logger's handlers
    # and propagate to root logger
    # noinspection PyUnresolvedReferences
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    sinks_ids = logger.configure(handlers=[{"sink": sys.stdout, "serialize": json_logs}])
    for sink_id in sinks_ids:
        logger.remove(sink_id)
    # logger.add(sys.stdout, level=log_level)

    logger_option = {
        "serialize": json_logs,
    }

    logger.add(sys.stdout, filter=LoggerFilter(level=log_level), **logger_option)
