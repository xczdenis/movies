from dataclasses import dataclass

from loguru import logger

from etl.models.es import Person
from etl.transformers.base import ESTransformer


@dataclass
class PersonTransformer(ESTransformer):
    index_name: str

    def transform_row(self, row_data) -> Person | None:
        try:
            return Person.parse_obj(row_data)
        except Exception as e:
            logger.error(
                "An error occurred during person data transformation. ID: %s. Error: %s"
                % (row_data.get("id"), e)
            )

        return None
