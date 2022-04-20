from pydamain.domain.models.main import aggregate, Aggregate


@aggregate
class Example(Aggregate):
    name: str


class TestAggregate:
    a1 = Example(name="a")
    a2 = Example(name="a")

    def test_aggregate_eq(self):
        assert Example.__eq__ == object.__eq__
        assert self.a1 != self.a2

    def test_aggregate_hash(self):
        assert Example.__hash__ == object.__hash__
        assert len({self.a1, self.a2}) == 2
