import abc


class IProcess:
    @abc.abstractmethod
    def start(self) -> None:
        pass
