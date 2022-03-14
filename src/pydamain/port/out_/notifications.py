from abc import abstractmethod, ABCMeta


class AbstractEmailNotification(metaclass=ABCMeta):
    @abstractmethod
    async def send(self, from_: str, to: str, subject: str, text: str) -> None:
        ...
