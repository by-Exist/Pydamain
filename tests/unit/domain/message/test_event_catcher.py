import pytest

from pydamain.domain import Event
from pydamain.domain.message.main import EventCatcher


class TestEventCatcher:
    def test_required_event_catcher(self):
        with pytest.raises(LookupError):
            Event().issue()

    def test_catch_event_nested(self):
        with EventCatcher() as ec1:
            Event().issue()
            with EventCatcher() as ec2:
                Event().issue()
                Event().issue()
                Event().issue()
            Event().issue()
        assert len(ec1.events) == 2
        assert len(ec2.events) == 3
    
    def test_catch_event_sibling(self):
        with (
            EventCatcher() as ec1,
            EventCatcher() as ec2,
            EventCatcher() as ec3,
        ):
            Event().issue()
            Event().issue()
            Event().issue()
        assert ec1.events == []
        assert ec2.events == []
        assert len(ec3.events) == 3
