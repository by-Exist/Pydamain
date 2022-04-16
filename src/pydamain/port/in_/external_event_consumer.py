from typing import Protocol


class ExternalEventConsumer(Protocol):
    async def consume(self):
        ...
