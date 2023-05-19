from abc import ABC, abstractmethod


class Loader(ABC):
    @abstractmethod
    def load(self, data, **kwargs) -> bool:
        ...
