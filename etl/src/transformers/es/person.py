# from dataclasses import dataclass
# from typing import Optional
#
# from loguru import logger
# from pg_to_es.models.es import Person
# from pg_to_es.transformers.base import ESBaseTransformer
#
#
# @dataclass
# class PersonTransformer(ESBaseTransformer):
#     index_name: str
#
#     def transform_row(self, row_data) -> Optional[Person]:
#         try:
#             return Person.parse_obj(row_data)
#         except Exception as e:
#             logger.error(
#                 "An error occurred during person data transformation. ID: {id}. Error: {error}".format(
#                     id=row_data.get("id"), error=e
#                 )
#             )
#
#         return None
