from dataclasses import FrozenInstanceError
from uuid import UUID, uuid4
import pytest

from pydamain.domain.messages import Command, command, field


@command
class Example(Command):
    id: UUID = field(default_factory=uuid4)
    name: str

    @property
    def identity(self):
        return self.id


class TestCommand:

    foo_1 = Example(name="foo")
    foo_2 = Example(name="foo")
    bar = Example(name="bar")

    def test_command_has_unique_id(self):
        assert self.foo_1 != self.foo_2

    def test_command_frozen(self):
        with pytest.raises(FrozenInstanceError):
            self.bar.name = "other"
