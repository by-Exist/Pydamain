from typing import Any, ClassVar

import pytest

from pydamain.domain import Event, EventHandlers


sync_flag = False
async_flag = False


def sync_handler(m: "ExEvent", **_: Any):
    global sync_flag
    sync_flag = True


async def async_handler(m: "ExEvent", **_: Any):
    global async_flag
    async_flag = True


nested_sync_flag = False
nested_async_flag = False


def nested_sync_handler(m: "ExNestedEvent", **_: Any):
    global nested_sync_flag
    nested_sync_flag = True


async def nested_async_handler(m: "ExNestedEvent", **_: Any):
    global nested_async_flag
    nested_async_flag = True


def sync_handler_raise_exception(m: "ExEvent", **_: Any):
    raise Exception()


async def async_handler_raise_exception(m: "ExEvent", **_: Any):
    raise Exception()


async def issue_nested_events(m: "ExEvent", **_: Any):
    ExNestedEvent().issue()


class ExEvent(Event):

    handlers: ClassVar[EventHandlers["ExEvent"]] = [
        sync_handler,
        async_handler,
        sync_handler_raise_exception,
        async_handler_raise_exception,
        issue_nested_events,
    ]


class ExNestedEvent(Event):

    handlers: ClassVar[EventHandlers["ExNestedEvent"]] = [
        nested_sync_handler,
        nested_async_handler,
    ]


class TestEvent:
    def test_need_event_catcher_context(self):
        e = ExEvent()
        with pytest.raises(LookupError):
            e.issue()

    async def test_handle(self):
        await ExEvent()._handle({})  # type: ignore
        assert sync_flag == True
        assert async_flag == True
        assert nested_sync_flag == True
        assert nested_async_flag == True

    @pytest.mark.skip(reason="NotImplemented")
    async def test_block_circular_event_issue(self):
        def issue_one(m: Event, **_: Any):
            OneEvent().issue()

        async def issue_two(m: Event, **_: Any):
            TwoEvent().issue()

        class OneEvent(Event):
            handlers: ClassVar[EventHandlers["OneEvent"]] = [issue_two]

        class TwoEvent(Event):
            handlers: ClassVar[EventHandlers["TwoEvent"]] = [issue_one]

        with pytest.raises(Exception):
            await OneEvent()._handle({})  # type: ignore
