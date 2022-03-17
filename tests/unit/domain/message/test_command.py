from typing import Any, ClassVar

from pydamain.domain import Command, Event, CommandHandler, EventHandlers


sync_cmd_handler_flag = False
async_cmd_handler_flag = False


def sync_cmd_handler(m: Command, **_: Any):
    global sync_cmd_handler_flag
    sync_cmd_handler_flag = True


async def async_cmd_handler(m: Command, **_: Any):
    global async_cmd_handler_flag
    async_cmd_handler_flag = True


sync_evt_handler_flag = False
async_evt_handler_flag = False


def sync_evt_handler(m: Event, **_: Any):
    global sync_evt_handler_flag
    sync_evt_handler_flag = True


async def async_evt_handler(m: Event, **_: Any):
    global async_evt_handler_flag
    async_evt_handler_flag = True


def sync_evt_raise_exception(m: Event, **_: Any):
    raise Exception()


async def async_evt_raise_exception(m: Event, **_: Any):
    raise Exception()


def issue_example_event(m: Command, **_: Any):
    ExampleEvent().issue()


class ExampleEvent(Event):

    handlers: ClassVar[EventHandlers["ExampleEvent"]] = [
        sync_evt_handler,
        async_evt_handler,
        sync_evt_raise_exception,
        async_evt_raise_exception,
    ]


class TestCommand:
    async def test_sync_handler_handle(self):
        class ExampleCommand(Command):
            handler: ClassVar[
                CommandHandler["ExampleCommand"]
            ] = sync_cmd_handler

        await ExampleCommand().handle({})
        assert sync_cmd_handler_flag == True

    async def test_async_handler_handle(self):
        class ExampleCommand(Command):
            handler: ClassVar[
                CommandHandler["ExampleCommand"]
            ] = async_cmd_handler

        await ExampleCommand().handle({})
        assert async_cmd_handler_flag == True

    async def test_handle_events_and_ignore_exception(self):
        class ExampleCommand(Command):
            handler: ClassVar[
                CommandHandler["ExampleCommand"]
            ] = issue_example_event

        await ExampleCommand().handle({})
        assert sync_evt_handler_flag == True
        assert async_evt_handler_flag == True
