from typing import cast
from uuid import UUID, uuid4

from pydamain.domain.messages import (
    Command,
    ExternalEvent,
    PublicEvent,
    command,
    external_event,
    field,
    public_event,
)


@public_event
class TestPublicEvent(PublicEvent):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id

    @property
    def from_(self):
        return None


@command
class TestCommand(Command):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id


@external_event
class Example(ExternalEvent):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id

    def build_commands(self) -> list[Command]:
        return [TestCommand(name=self.name)]


class TestExternalEvent:
    def test_flow(self):
        published_event = TestPublicEvent(name="blabla...")
        message = published_event.dumps()
        external_event = Example.loads(message)
        cmd = external_event.build_commands()[0]
        cmd = cast(TestCommand, cmd)
        assert cmd.name == "blabla..."
