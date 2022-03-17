from typing import Any, ClassVar, cast

from aiokafka import AIOKafkaConsumer  # type: ignore

from pydantic import BaseModel

from pydamain.domain import Event
from pydamain.adapter.out_.event_producer import jsonb_to_event
from pydamain.port.in_.event_consumer import AbstractEventConsumer


class KafkaEvent(BaseModel):
    event_type: bytes
    event: bytes


class BaseKafkaEventConsumer(AbstractEventConsumer):

    host: ClassVar[str]
    port: ClassVar[int]
    topic: ClassVar[str]

    def __init__(self, deps: dict[str, Any]) -> None:
        self.aiokafka_consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=f"{self.host}:{self.port}",
            value_deserializer=jsonb_to_event,
            group_id=type(self).__name__,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
        )
        self.deps = deps

    def pre_consume(self, event: Event):
        ...

    def post_consume(self, event: Event):
        ...

    async def consume(self):
        async for event in self.aiokafka_consumer:  # type: ignore
            event = cast(Event, event)
            self.pre_consume(event)
            await event._handle(self.deps)  # type: ignore
            await self.aiokafka_consumer.commit()  # type: ignore
            self.post_consume(event)
