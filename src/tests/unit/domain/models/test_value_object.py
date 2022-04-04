from dataclasses import FrozenInstanceError
import pytest
from pydamain.domain.models.main import value_object, ValueObject


@value_object
class Example(ValueObject):
    name: str


class TestValueObject:

    foo_1 = Example(name="foo")
    foo_2 = Example(name="foo")
    bar = Example(name="bar")

    def test_value_object_eq(self):
        assert self.foo_1 == self.foo_2
        assert self.foo_1 != self.bar

    def test_value_object_hash(self):
        assert len({self.foo_1, self.foo_2}) == 1
        assert len({self.foo_1, self.bar}) == 2

    def test_value_object_frozen(self):
        with pytest.raises(FrozenInstanceError):
            self.foo_1.name = "other"
