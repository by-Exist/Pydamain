from typing import Any

import pytest

from pydamain.domain.messages.message import Message, MessageCatchContext, issue


class ExampleMessage(Message):
    async def handle_(self, deps: dict[str, Any]) -> Any:
        ...


def test_hook():
    m1 = ExampleMessage()
    m2 = ExampleMessage()
    with MessageCatchContext() as message_catcher:
        issue(m1)
        issue(m2)
        issue(m2)
    assert {m1, m2} == message_catcher.messages


def test_hook_without_catcher():
    m = ExampleMessage()
    with pytest.raises(LookupError):
        issue(m)
