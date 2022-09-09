import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    PROJECT_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    LOG_LEVEL: str = "DEBUG"
    JSON_LOGS: bool = False

    class Config:
        env_file = os.path.join(ROOT_DIR, ".envs", "development", ".env")
        env_file_encoding = "utf-8"


settings = Settings()
