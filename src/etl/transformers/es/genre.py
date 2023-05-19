from dataclasses import dataclass

from loguru import logger

from etl.models.es import Genre
from etl.transformers.base import ESTransformer


@dataclass
class GenreTransformer(ESTransformer):
    index_name: str

    def transform_row(self, row_data) -> Genre | None:
        try:
            return Genre.parse_obj(row_data)
        except Exception as e:
            logger.error(
                "An error occurred during genre data transformation. ID: %s. Error: %s"
                % (row_data.get("id"), e)
            )
        return None
