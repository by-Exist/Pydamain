from contextvars import ContextVar
from typing import Any, ClassVar, Iterable, TypeVar, cast
from weakref import WeakValueDictionary
import asyncio

from .base import BaseMessage
from .typing import AsyncHandler, Handler, SyncHandler


# ============================================================================
# Command
# ============================================================================
FirstPosOnlyArgType = TypeVar("FirstPosOnlyArgType")
CommandHandler = Handler[FirstPosOnlyArgType, Any] | None


class Command(BaseMessage):

    handler: ClassVar[CommandHandler[Any]] = None

    async def handle(self, deps: dict[str, Any]):
        events = await asyncio.create_task(self._handle(deps))
        await asyncio.gather(
            *(event.handle(deps) for event in events), return_exceptions=True
        )

    async def _handle(self, deps: dict[str, Any]):
        if not self.handler:
            return list[Event]()
        with EventCatcher() as event_catcher:
            await handles_message(self, self.handler, deps)
        return event_catcher.events


# ============================================================================
# Event
# ============================================================================
EventHandlers = Iterable[Handler[FirstPosOnlyArgType, Any]]


class Event(BaseMessage):

    handlers: ClassVar[EventHandlers[Any]] = []

    __event_type_registry__: ClassVar[
        WeakValueDictionary[str, type["Event"]]
    ] = WeakValueDictionary()

    def __init_subclass__(cls) -> None:
        cls.handlers = set(cls.handlers)
        cls.__event_type_registry__[cls.__name__] = cls

    def issue(self):
        event_list = events_context_var.get()
        event_list.append(self)

    async def handle(self, deps: dict[str, Any]):
        events = await asyncio.create_task(self._handle(deps))
        await asyncio.gather(
            *(event.handle(deps) for event in events), return_exceptions=True
        )

    async def _handle(self, deps: dict[str, Any]):
        with EventCatcher() as event_catcher:
            await asyncio.gather(
                *(
                    handles_message(self, handler, deps)
                    for handler in self.handlers
                ),
                return_exceptions=True,
            )
        return event_catcher.events


# ============================================================================
# Handle Function
# ============================================================================
M = TypeVar("M", bound=BaseMessage)
R = TypeVar("R")


async def handles_message(
    msg: M, handler: Handler[M, R], deps: dict[str, Any]
) -> R:
    if asyncio.iscoroutinefunction(handler):
        handler = cast(AsyncHandler[M, R], handler)
        return await handler(msg, **deps)
    handler = cast(SyncHandler[M, R], handler)
    return await asyncio.to_thread(handler, msg, **deps)


# ============================================================================
# Event Catcher
# ============================================================================
events_context_var: ContextVar[list[Event]] = ContextVar("events_context_var")


class EventCatcher:
    def __init__(self):
        self.events: list[Event] = []

    def __enter__(self):
        self.token = events_context_var.set(list())
        return self

    def __exit__(self, *args: tuple[Any]):
        self.events.extend(events_context_var.get())
        events_context_var.reset(self.token)
