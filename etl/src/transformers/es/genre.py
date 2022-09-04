from dataclasses import dataclass
from typing import Optional

from loguru import logger
from models.es import Genre
from transformers.interface import IESTransformer


@dataclass
class GenreTransformer(IESTransformer):
    index_name: str

    def transform_row(self, row_data) -> Optional[Genre]:
        try:
            return Genre.parse_obj(row_data)
        except Exception as e:
            logger.error(
                "An error occurred during genre data transformation. ID: {id}. Error: {error}".format(
                    id=row_data.get("id"), error=e
                )
            )

        return None
