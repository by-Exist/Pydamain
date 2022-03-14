from contextvars import ContextVar
from datetime import datetime
from typing import ClassVar
from uuid import uuid4
from weakref import WeakValueDictionary
import asyncio

from loguru import logger
from pydantic import BaseModel, Field, UUID4

from pydamain.typing import (
    Any,
    AsyncHandler,
    Handler,
    SyncHandler,
    TypeVar,
    cast,
)
from pydamain.domain.model import Aggregate


class BaseMessage(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    create_time: datetime = Field(default_factory=datetime.now)

    class Config:
        frozen = True


R = TypeVar("R")


class Command(BaseMessage):

    handler: ClassVar[Handler["Command", Any] | None] = None

    async def handle(self, deps: dict[str, Any]):
        events = await asyncio.create_task(self._handle(deps))
        await asyncio.gather(
            *(event.handle(deps) for event in events), return_exceptions=True
        )

    async def _handle(self, deps: dict[str, Any]):
        if not self.handler:
            logger.debug(f"{type(self).__name__} is not have handler.")
            return []  # type: ignore
        with EventContext() as event_catcher:
            await handle_message(self, self.handler, deps)
        return event_catcher.events


class Event(BaseMessage):

    from_: Aggregate | None = Field(None, exclude=True)

    handlers: ClassVar[set[Handler["Event", Any]]] = set()

    __event_type_registry__: ClassVar[
        WeakValueDictionary[str, type["Event"]]
    ] = WeakValueDictionary()  # need deserialization from external event

    def __init_subclass__(cls) -> None:
        event_registry[cls.__name__] = cls

    def issue(self):
        event_list = events_context_var.get()
        event_list.append(self)

    async def handle(self, deps: dict[str, Any]):
        events = await asyncio.create_task(self._handle(deps))
        await asyncio.gather(
            *(event.handle(deps) for event in events), return_exceptions=True
        )

    async def _handle(self, deps: dict[str, Any]):
        if not self.handlers:
            logger.debug(f"{type(self).__name__} is not have handlers.")
            return []  # type: ignore
        with EventContext() as event_catcher:
            await asyncio.gather(
                *(
                    handle_message(self, handler, deps)
                    for handler in self.handlers
                ),
                return_exceptions=True,
            )
        return event_catcher.events


event_registry: WeakValueDictionary[str, type["Event"]] = WeakValueDictionary()


def deserialize_external_event(type_: bytes, json: bytes):
    event_cls = event_registry[type_.decode("utf-8")]
    return event_cls.parse_raw(json)


events_context_var: ContextVar[list[Event]] = ContextVar("events_context_var")


class EventContext:
    def __init__(self):
        self.events: list[Event] = []

    def __enter__(self):
        self.token = events_context_var.set(list())
        return self

    def __exit__(self, *args: tuple[Any]):
        self.events.extend(events_context_var.get())
        events_context_var.reset(self.token)


M = TypeVar("M")


async def handle_message(
    msg: M,
    handler: Handler[M, R],
    deps: dict[str, Any],
):
    try:
        logger.debug(f"Handling {msg} with handler {handler.__name__}")
        if asyncio.iscoroutinefunction(handler):
            handler = cast(AsyncHandler[M, R], handler)
            await handler(msg, **deps)
        else:
            handler = cast(SyncHandler[M, R], handler)
            await asyncio.to_thread(handler, msg, **deps)
    except Exception as e:
        logger.exception(f"Exception handling {msg}")
        raise e
