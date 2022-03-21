from abc import abstractmethod, ABCMeta


class AbstractNotification(metaclass=ABCMeta):
    @abstractmethod
    async def send(self, from_: str, to: str, subject: str, text: str) -> None:
        ...
