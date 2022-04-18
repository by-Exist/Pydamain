from typing import Any
from pydamain.domain.models.main import entity, Entity


@entity
class Example(Entity[Any]):
    name: str


class TestValueObject:
    a1 = Example(name="a")
    a2 = Example(name="a")

    def test_entity_eq(self):
        assert Example.__eq__ is object.__eq__
        assert self.a1 != self.a2

    def test_entity_hash(self):
        assert Example.__hash__ is object.__hash__
        assert len({self.a1, self.a2}) == 2