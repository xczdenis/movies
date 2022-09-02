import abc
from typing import Iterator


class IExtractor:
    @abc.abstractmethod
    def extract(self) -> Iterator[any]:
        pass
