import os
from pathlib import Path

import const
from models import pg as pg_models
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Config(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_EXTRACTOR_BATCH_SIZE = 500
    POSTGRES_SCHEME = "content"

    SQLITE_EXTRACTOR_BATCH_SIZE = 500

    ELASTIC_HOST: str
    ELASTIC_PORT: str

    PG_TO_ES_REPEAT_INTERVAL: int = 0

    ES_INDEXES = {
        const.INDEX_MOVIES: os.path.join(BASE_DIR, "assets/es_indexes_schemas/movies.json"),
        const.INDEX_GENRES: os.path.join(BASE_DIR, "assets/es_indexes_schemas/genres.json"),
        const.INDEX_PERSONS: os.path.join(BASE_DIR, "assets/es_indexes_schemas/persons.json"),
    }

    TABLES_MAPPING = {
        const.TABLE_GENRE: pg_models.Genre,
        const.TABLE_PERSON: pg_models.Person,
        const.TABLE_FILMWORK: pg_models.Filmwork,
        const.TABLE_GENRE_FILMWORK: pg_models.GenreFilmwork,
        const.TABLE_PERSON_FILMWORK: pg_models.PersonFilmwork,
    }

    class Config:
        env = os.getenv("ENVIRONMENT", "development")
        env_file = os.path.join(ROOT_DIR, ".envs", env, ".env")
        env_file_encoding = "utf-8"


config = Config()
