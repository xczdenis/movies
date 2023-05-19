import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent


class BaseSettingsConfigMixin(BaseSettings):
    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(BaseSettingsConfigMixin):
    ENVIRONMENT: str = "production"
    SECRET_KEY: str
    ALLOWED_HOSTS: str
    CSRF_TRUSTED_ORIGINS: str
    SUPERUSER_LOGIN: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str


class PGSettings(BaseSettingsConfigMixin):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int


# config = Settings()
app_settings: AppSettings = AppSettings()
pg_settings: PGSettings = PGSettings()
