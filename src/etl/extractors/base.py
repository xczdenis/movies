from abc import ABC, abstractmethod
from typing import Generator


class Extractor(ABC):
    @abstractmethod
    def extract(self, *args, **kwargs) -> Generator:
        ...
