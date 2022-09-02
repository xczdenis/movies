import abc
from typing import Callable, Optional


class ILoader:
    post_load_handler: Optional[Callable]

    @abc.abstractmethod
    def load(self, data: any) -> bool:
        pass
