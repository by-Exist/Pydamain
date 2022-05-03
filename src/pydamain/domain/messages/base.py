from abc import ABCMeta, abstractmethod
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any, Optional, final


@dataclass(frozen=True, kw_only=True, slots=True)
class Message(metaclass=ABCMeta):
    @abstractmethod
    async def handle_(self, deps: dict[str, Any]) -> Any:
        ...

    @final
    def hook_(self):
        messages = messages_context_var.get()
        messages.add(self)


messages_context_var: ContextVar[set[Message]] = ContextVar("messages")


@dataclass(slots=True)
class MessageCatchContext:

    messages: set[Message] = field(default_factory=set, init=False)
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
        self.messages = messages_context_var.get()
        messages_context_var.reset(self._token)
