from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, cast
from aiokafka import AIOKafkaConsumer, ConsumerRecord  # type: ignore

from ...port.in_.external_event_consumer import ExternalEventConsumer

if TYPE_CHECKING:
    from ...domain.service import MessageBus
    from ...domain.messages import ExternalEvent


@dataclass
class BaseKafkaExternalEventConsumer(ExternalEventConsumer):

    BOOTSTRAP_SERVERS: ClassVar[list[str]]
    GROUP_ID: ClassVar[str]
    TOPIC_NAME_EXTERNAL_EVENT_TYPE_MAP: ClassVar[dict[str, type[ExternalEvent]]]

    bus: MessageBus
    _aiokafka_consumer: AIOKafkaConsumer = field(init=False)

    def __post_init__(self):
        self._aiokafka_consumer = AIOKafkaConsumer(
            *self.TOPIC_NAME_EXTERNAL_EVENT_TYPE_MAP.keys(),
            bootstrap_servers=self.BOOTSTRAP_SERVERS,
            group_id=self.GROUP_ID,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            isolation_level="read_committed",
        )

    async def pre_consume(self, external_event: ExternalEvent):
        ...

    async def post_consume(self, external_event: ExternalEvent):
        ...

    async def consume(self):
        await self._aiokafka_consumer.start()
        try:
            async for record in self._aiokafka_consumer:  # type: ignore
                record = cast(ConsumerRecord[bytes, bytes], record)
                if not record.value:
                    continue
                external_event = self.deserialize_value(record.topic, record.value)
                await self.pre_consume(external_event)
                for command in external_event.build_commands_():
                    await self.bus.handle(command)
                await self.post_consume(external_event)
                await self._aiokafka_consumer.commit()  # type: ignore
        finally:
            await self._aiokafka_consumer.stop()

    @classmethod
    def deserialize_value(cls, topic: str, value: bytes):
        external_event_type = cls.TOPIC_NAME_EXTERNAL_EVENT_TYPE_MAP[topic]
        return external_event_type.load_(value)
