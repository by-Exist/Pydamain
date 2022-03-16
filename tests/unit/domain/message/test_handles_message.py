from typing import Any

from pydamain.domain.message.base import BaseMessage
from pydamain.domain.message.main import handles_message


sync_flag = False
async_flag = False


def sync_handler(m: "ExampleMessage", **_: Any):
    global sync_flag
    sync_flag = True
    return "runned sync handler"


def async_handler(m: "ExampleMessage", **_: Any):
    global async_flag
    async_flag = True
    return "runned async handler"


class ExampleMessage(BaseMessage):
    ...


class TestHandleMessage:
    async def test_handle_sync(self):
        m = ExampleMessage()
        result = await handles_message(m, sync_handler, {})
        assert sync_flag
        assert result == "runned sync handler"

    async def test_handle_async(self):
        m = ExampleMessage()
        result = await handles_message(m, async_handler, {})
        assert async_flag
        assert result == "runned async handler"
