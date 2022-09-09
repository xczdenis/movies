from models.genre import Genre
from models.mixins import BaseModelWithMeta, OrjsonConfigMixin, UUIDMixin
from models.person import Person


class Film(BaseModelWithMeta, UUIDMixin, OrjsonConfigMixin):
    title: str
    rating: float
    description: str = ""
    genres: list[Genre] = []
    actors: list[Person] = []
    writers: list[Person] = []
    director: str = ""

    class Meta:
        index = "movies"
