import os
from pathlib import Path

from pydantic import BaseSettings

from etl.config import constants
from etl.models import pg as pg_models

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent


class BaseSettingsConfigMixin(BaseSettings):
    class Config:
        env_file = os.path.join(ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


class PGConfig(BaseSettingsConfigMixin):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_EXTRACTOR_BATCH_SIZE = 500
    POSTGRES_SCHEME = "content"


class SQLiteConfig(BaseSettingsConfigMixin):
    SQLITE_EXTRACTOR_BATCH_SIZE = 500
    DATABASE_PATH = os.path.join(ROOT_DIR, "files", "fake-db.sqlite")


class ElasticConfig(BaseSettingsConfigMixin):
    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_USER: str
    ELASTIC_PASSWORD: str

    ES_INDEXES = {
        constants.INDEX_MOVIES: os.path.join(BASE_DIR, "assets", "es_indexes_schemas", "movies.json"),
        constants.INDEX_GENRES: os.path.join(BASE_DIR, "assets", "es_indexes_schemas", "genres.json"),
        constants.INDEX_PERSONS: os.path.join(BASE_DIR, "assets", "es_indexes_schemas", "persons.json"),
    }


class RedisConfig(BaseSettingsConfigMixin):
    REDIS_HOST: str
    REDIS_PORT: int


class BaseConfig(BaseSettingsConfigMixin):
    TABLES_MAPPING = {
        constants.TABLE_GENRE: pg_models.Genre,
        constants.TABLE_PERSON: pg_models.Person,
        constants.TABLE_FILMWORK: pg_models.Filmwork,
        constants.TABLE_GENRE_FILMWORK: pg_models.GenreFilmwork,
        constants.TABLE_PERSON_FILMWORK: pg_models.PersonFilmwork,
    }


pg_config: PGConfig = PGConfig()
sqlite_config: SQLiteConfig = SQLiteConfig()
base_config: BaseConfig = BaseConfig()
es_config: ElasticConfig = ElasticConfig()
redis_config: RedisConfig = RedisConfig()
