import os
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    SEARCH_APP_HOST: str = Field(default="127.0.0.1")
    SEARCH_APP_PORT: int = Field(default="8000")
    PROJECT_NAME: str
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
        env = os.getenv("ENVIRONMENT", "development")
        env_file = os.path.join(ROOT_DIR, ".envs", env, ".env"), os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()
