from abc import abstractmethod, ABCMeta

from pydamain.domain import Event


class AbstractEventProducer(metaclass=ABCMeta):
    @abstractmethod
    async def send(self, event: Event):
        ...
