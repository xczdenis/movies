import abc
from dataclasses import dataclass
from typing import Iterator


class ITransformer:
    @abc.abstractmethod
    def transform(self, data: Iterator) -> list[any]:
        pass

    @staticmethod
    def normalize_value(value, type):
        if value is None:
            if type == int:
                return 0
            if type == float:
                return 0.0
            elif type == str:
                return ""
        return value


@dataclass
class IESTransformer(ITransformer):
    index_name: str

    def transform(self, data: Iterator):
        transformed_data = []
        for row in data:
            instance_of_model = self.transform_row(row)
            if instance_of_model:
                transformed_data += [
                    {"index": {"_index": self.index_name, "_id": instance_of_model.id}},
                    instance_of_model.dict(exclude={"title"}),
                ]
        return transformed_data

    @abc.abstractmethod
    def transform_row(self, data: Iterator):
        pass
