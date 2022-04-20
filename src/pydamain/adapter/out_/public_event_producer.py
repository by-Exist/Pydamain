from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar
from uuid import UUID

from aiokafka import AIOKafkaProducer  # type: ignore
from aiokafka.structs import RecordMetadata  # type: ignore

from ...port.out_.public_event_producer import PublicEventProducer


if TYPE_CHECKING:
    from ...domain.messages import PublicEvent


@dataclass
class BaseKafkaPublicEventProducer(PublicEventProducer):

    BOOTSTRAP_SERVERS: ClassVar[list[str]]
    TOPIC_PREFIX: ClassVar[list[str]]

    _aiokafka_producer: AIOKafkaProducer = field(init=False)

    def __post_init__(self):
        self._aiokafka_producer = AIOKafkaProducer(
            bootstrap_servers=self.BOOTSTRAP_SERVERS,
            enable_idempotence=True,
        )

    async def pre_send(self, msg: PublicEvent):
        ...

    async def post_send(self, msg: PublicEvent):
        ...

    async def send(self, public_event: PublicEvent):
        await self._aiokafka_producer.start()
        await self.pre_send(public_event)
        record_metadata: RecordMetadata = await self._aiokafka_producer.send_and_wait(  # type: ignore
            topic=self.build_topic_name(public_event),
            key=self.serialize_key(public_event.from_) if public_event.from_ else None,
            value=self.serialize_value(public_event),
        )
        await self.post_send(public_event)
        await self._aiokafka_producer.stop()

    @classmethod
    def build_topic_name(cls, public_event: PublicEvent):
        return f"{cls.TOPIC_PREFIX}/{type(public_event).__name__}"

    @classmethod
    def serialize_key(cls, id: UUID):
        return id.bytes

    @classmethod
    def serialize_value(cls, public_event: PublicEvent):
        return public_event.dumps()
