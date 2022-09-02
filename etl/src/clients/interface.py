import abc


class IClient:
    @abc.abstractmethod
    def connect(self):
        pass
