from dataclasses import FrozenInstanceError
import pytest
from pydamain.domain.messages.main import Command, command


@command
class Example(Command):
    name: str


class TestCommand:

    foo_1 = Example(name="foo")
    foo_2 = Example(name="foo")
    bar = Example(name="bar")

    def test_command_has_unique_id(self):
        assert self.foo_1 != self.foo_2

    def test_command_frozen(self):
        with pytest.raises(FrozenInstanceError):
            self.bar.name = "other"
