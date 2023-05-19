import os
from pathlib import Path

from pydantic import BaseSettings, validator

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    CONTENT_APP_HOST: str
    CONTENT_APP_PORT: int
    BASE_API_PREFIX: str = "api"
    API_V1_PREFIX: str = "v1"
    ELASTIC_USER: str
    ELASTIC_PASSWORD: str
    PROJECT_NAME: str
    DEBUG: bool = False
    RELOAD: bool = False
    REDIS_HOST: str
    REDIS_PORT: int
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    LOG_LEVEL: str = "DEBUG"
    JSON_LOGS: bool = False
    TESTS_MAX_FILMS_NUMBER: int = 50
    TESTS_MAX_PERSONS_NUMBER: int = 50
    TESTS_MAX_GENRES_NUMBER: int = 50

    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"

    @validator("DEBUG")
    def set_debug(cls, v, values):  # noqa
        return v and values["ENVIRONMENT"] == "development"

    @validator("RELOAD")
    def set_reload(cls, v, values):  # noqa
        return v and values["ENVIRONMENT"] == "development"


settings: Settings = Settings()
