from contextvars import ContextVar
from typing import Any, ClassVar, Iterable, TypeVar, cast
from weakref import WeakValueDictionary
import asyncio

from .base import BaseMessage
from .typing import AsyncHandler, Handler, SyncHandler


# ============================================================================
# Command
# ============================================================================
C = TypeVar("C", bound="Command")
CommandHandler = Handler[C, Any]


class Command(BaseMessage):

    handler: ClassVar[CommandHandler[Any]] = None  # type: ignore

    async def handle(self, deps: dict[str, Any]):
        self.pre_handle()
        events = await asyncio.create_task(self._handle(deps))
        self.post_handle()
        await handle_events(events, deps)

    async def _handle(self, deps: dict[str, Any]):
        if not self.handler:
            return list[Event]()
        with EventCatcher() as event_catcher:
            await handle(self, type(self).handler, deps)
        return event_catcher.events


# ============================================================================
# Event
# ============================================================================
E = TypeVar("E", bound="Event")
EventHandlers = Iterable[Handler[E, Any]]


class Event(BaseMessage):

    handlers: ClassVar[EventHandlers[Any]] = []

    __event_subclass_registry__: ClassVar[
        WeakValueDictionary[str, type["Event"]]
    ] = WeakValueDictionary()

    def __init_subclass__(cls) -> None:
        cls.handlers = set(cls.handlers)
        cls.__event_subclass_registry__[cls.__name__] = cls

    def issue(self):
        event_list = events_context_var.get()
        event_list.append(self)

    async def _handle(self, deps: dict[str, Any]):
        self.pre_handle()
        events = await asyncio.create_task(self.__handle(deps))
        self.post_handle()
        await handle_events(events, deps)

    async def __handle(self, deps: dict[str, Any]):
        with EventCatcher() as event_catcher:
            await asyncio.gather(
                *(handle(self, handler, deps) for handler in self.handlers),
                return_exceptions=True,
            )
        return event_catcher.events


async def handle_events(
    events: Iterable[Event],
    deps: dict[str, Any],
    ignore_exception: bool = True,
):
    coros = (event._handle(deps) for event in events)  # type: ignore
    await asyncio.gather(*coros, return_exceptions=ignore_exception)


# ============================================================================
# Handle Function
# ============================================================================
M = TypeVar("M", bound=BaseMessage)
R = TypeVar("R")


async def handle(msg: M, handler: Handler[M, R], deps: dict[str, Any]) -> R:
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
