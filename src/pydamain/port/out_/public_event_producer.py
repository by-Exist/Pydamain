from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ...domain.messages import PublicEvent


class PublicEventProducer(Protocol):
    async def send(self, _msg: PublicEvent):
        ...