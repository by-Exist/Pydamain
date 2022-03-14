from abc import abstractmethod, ABCMeta


class AbstractEventConsumer(metaclass=ABCMeta):
    @abstractmethod
    async def consume(self):
        ...
