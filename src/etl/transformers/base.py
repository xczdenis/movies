import abc
from dataclasses import dataclass
from typing import Generator, Iterator


class Transformer(abc.ABC):
    @abc.abstractmethod
    def transform(self, data) -> Generator:
        ...


@dataclass
class ESTransformer(Transformer):
    index_name: str

    def transform(self, data: Iterator):
        transformed_data = []
        for row in data:
            instance_of_model = self.transform_row(row)
            if instance_of_model:
                transformed_data += [
                    {"index": {"_index": self.index_name, "_id": instance_of_model.id}},
                    instance_of_model.dict(),
                ]
        return transformed_data

    @abc.abstractmethod
    def transform_row(self, data: Iterator):
        pass
