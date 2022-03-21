import pytest

from pydamain.domain.model.base import ValueObject


class ExampleValueObject(ValueObject):
    text: str


class TestValueObject:
    def test_immutable(self):
        with pytest.raises(TypeError):
            evo = ExampleValueObject(text="first")
            evo.text = "second"

    def test_jsonable(self):
        assert ExampleValueObject(text="first").json() == r'{"text":"first"}'

    def test_equality(self):
        assert ExampleValueObject(text="same") == ExampleValueObject(
            text="same"
        )
        assert ExampleValueObject(text="first") != ExampleValueObject(
            text="second"
        )
