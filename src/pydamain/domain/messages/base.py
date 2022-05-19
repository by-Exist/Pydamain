from abc import ABCMeta
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any, Optional

from typing_extensions import Self, dataclass_transform


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
class MessageMeta(ABCMeta):
    def __new__(
        cls: type[Self], name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> Self:
        new_cls = super().__new__(cls, name, bases, namespace)
        return dataclass(frozen=True, kw_only=True)(new_cls)  # type: ignore


class Message(metaclass=MessageMeta):
    ...


def issue(message: Message):
    messages = messages_context_var.get()
    messages.add(message)


def get_issued_messages():
    return messages_context_var.get()


messages_context_var: ContextVar[set[Message]] = ContextVar("messages")


@dataclass(slots=True)
class MessageCatchContext:

    _token: Token[set[Message]] = field(init=False)

    def __enter__(self):
        self._token = messages_context_var.set(set())
        return self

    def __exit__(
        self,
        __exc_type: Optional[type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        messages_context_var.reset(self._token)
