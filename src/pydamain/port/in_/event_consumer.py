from abc import ABCMeta, abstractmethod


class AbstractEventConsumer(metaclass=ABCMeta):
    @abstractmethod
    async def consume(self):
        ...
