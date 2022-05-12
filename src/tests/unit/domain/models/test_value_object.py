from dataclasses import FrozenInstanceError
import pytest
from pydamain.domain.models import ValueObject


class Example(ValueObject):
    name: str


def test_value_object_eq():
    assert Example(name="foo") == Example(name="foo")
    assert Example(name="foo") != Example(name="bar")


def test_value_object_hash():
    assert len({Example(name="foo"), Example(name="foo")}) == 1
    assert len({Example(name="foo"), Example(name="bar")}) == 2


def test_value_object_frozen():
    with pytest.raises(FrozenInstanceError):
        Example(name="foo").name = "other"
