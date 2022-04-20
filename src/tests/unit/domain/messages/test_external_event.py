from typing import cast

from pydamain.domain.messages import (
    Command,
    ExternalEvent,
    PublicEvent,
    command,
    external_event,
    public_event,
)


@public_event
class PublicEvent(PublicEvent):
    name: str


@command
class TestCommand(Command):
    name: str


@external_event
class Example(ExternalEvent):

    name: str

    def build_commands(self) -> list[Command]:
        return [TestCommand(name=self.name)]


class TestExternalEvent:
    def test_flow(self):
        published_event = PublicEvent(name="blabla...")
        message = published_event.dumps()
        external_event = Example.loads(message)
        cmd = external_event.build_commands()[0]
        cmd = cast(TestCommand, cmd)
        assert (
            published_event.id == external_event.id
            and published_event.create_time == external_event.create_time
        )
        assert published_event.create_time != cmd.create_time
        assert cmd.name == "blabla..."