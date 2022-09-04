import abc
from typing import Iterator, Optional


class IExtractor:
    @abc.abstractmethod
    def extract(self) -> Optional[Iterator[any]]:
        pass
