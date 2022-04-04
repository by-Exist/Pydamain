from abc import ABCMeta, abstractmethod

from ...domain.messages import PublicEvent


class AbstractEventPublisher(metaclass=ABCMeta):
    @abstractmethod
    async def publish(self, public_event: PublicEvent):
        ...
