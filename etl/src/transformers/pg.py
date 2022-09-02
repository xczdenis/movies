from dataclasses import dataclass
from typing import Iterator

from transformers.interface import ITransformer


@dataclass
class PGTransformer(ITransformer):
    model: dataclass

    def transform(self, data: Iterator) -> list:
        transformed_data = []
        for row in data:
            transformed_data.append(self.__get_values_in_key_order(row))
        return transformed_data

    def __get_values_in_key_order(self, row: dict) -> tuple:
        _data = {}
        for field_name, field in self.model.__dataclass_fields__.items():
            _data[field_name] = ITransformer.normalize_value(row[field_name], field.type)
        return tuple(_data.values())
