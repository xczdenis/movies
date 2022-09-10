import orjson
from loguru import logger
from models.utils import orjson_dumps
from pydantic import BaseModel


class BaseModelWithMeta(BaseModel):
    @property
    def pk(self):
        if hasattr(self, "id"):
            return self.id
        elif hasattr(self, "uuid"):
            return self.uuid
        raise AttributeError(f"Unable to get 'pk' from object '{self.__repr__()[:150]}...'")

    @classmethod
    def get_index_name(cls):
        index = ""
        try:
            index = cls.Meta.index
        except Exception as e:
            logger.error(e)

        if not index:
            logger.info(
                "Unable to get index from model {model}. "
                "Maybe you forget to add class Meta into model {model}.".format(model=cls.__name__)
            )

        return index

    class Meta:
        index = ""


class UUIDMixin(BaseModel):
    id: str


class OrjsonConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
