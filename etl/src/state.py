import abc
import json
from typing import Any, Optional

from loguru import logger


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(e)
            pass
        return {}


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        state = self.storage.retrieve_state()
        state.update({key: value})
        self.storage.save_state(state)
        return None

    def get_state(self, key: str) -> Any:
        return self.storage.retrieve_state().get(key)


class MovieStorage(State):
    KEY_UPDATED_AT_MOVIES = "last_updated_at_movies"
    KEY_UPDATED_AT_GENRES = "last_updated_at_genres"
    KEY_UPDATED_AT_PERSONS = "last_updated_at_persons"

    def __init__(self, path_to_json: str):
        super().__init__(JsonFileStorage(path_to_json))

    def set_last_update_movie(self, **kwargs):
        self.set_state_from_row_data(MovieStorage.KEY_UPDATED_AT_MOVIES, "updated_at", **kwargs)

    def set_last_update_genres(self, **kwargs):
        self.set_state_from_row_data(MovieStorage.KEY_UPDATED_AT_GENRES, "updated_at", **kwargs)

    def set_last_update_persons(self, **kwargs):
        self.set_state_from_row_data(MovieStorage.KEY_UPDATED_AT_PERSONS, "updated_at", **kwargs)

    def get_last_update_movie(self):
        return self.get_state(MovieStorage.KEY_UPDATED_AT_MOVIES)

    def get_last_update_genres(self):
        return self.get_state(MovieStorage.KEY_UPDATED_AT_GENRES)

    def get_last_update_persons(self):
        return self.get_state(MovieStorage.KEY_UPDATED_AT_PERSONS)

    def set_state_from_row_data(self, state_key, row_data_key, **kwargs):
        success = kwargs.get("success", False)
        row_data = kwargs.get("row_data", False)
        if success:
            last_updated_at = row_data[-1].get(row_data_key)
            if last_updated_at:
                self.set_state(state_key, str(last_updated_at))
