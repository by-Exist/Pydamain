from uuid import uuid4
import pytest

from pydamain.domain.model.base import Entity


class ExampleEntity(Entity):
    text: str


class TestEntity:
    def test_id_immutable(self):
        with pytest.raises(TypeError):
            ee = ExampleEntity(text="first")
            ee.id = uuid4()

    def test_id_equality(self):
        same_id = uuid4()
        first = ExampleEntity(id=same_id, text="first")
        second = ExampleEntity(id=same_id, text="second")
        assert first == second

    def test_id_hashing(self):
        same_id = uuid4()
        first = ExampleEntity(id=same_id, text="first")
        second = ExampleEntity(id=same_id, text="second")
        assert len(set([first, second])) == 1

    def test_jsonable(self):
        origin_id = uuid4()
        assert (
            ExampleEntity(id=origin_id, text="first").json()
            == f"""{{"id":"{origin_id}","text":"first"}}"""
        )
