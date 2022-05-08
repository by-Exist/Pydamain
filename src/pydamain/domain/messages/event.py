from dataclasses import dataclass, field
from typing import Any, ClassVar, Iterable, TypeVar
import asyncio

from typing_extensions import Self, dataclass_transform

from .base import Message
from .typing_ import Handler


SelfEvent = TypeVar("SelfEvent", bound="Event")
EventHandler = Handler[SelfEvent, Any]
EventHandlers = Iterable[EventHandler[SelfEvent]]


@dataclass(frozen=True, kw_only=True, slots=True)
class Event(Message):

    HANDLERS: ClassVar[EventHandlers[Self]]

    async def _pre_handle(self, handler: EventHandler[Self]):
        ...

    async def _post_handle(self, handler: EventHandler[Self]):
        ...

    async def handle_(self, deps: dict[str, Any]):
        handlers = type(self).HANDLERS
        coros = (self._handle(handler, deps) for handler in handlers)
        return await asyncio.gather(*coros, return_exceptions=True)

    async def _handle(self, handler: EventHandler[Self], deps: dict[str, Any]) -> Any:
        await self._pre_handle(handler)
        result = await handler(self, **deps)
        await self._post_handle(handler)
        return result


@dataclass_transform(
    eq_default=True,
    order_default=False,
    kw_only_default=True,
    field_descriptors=(field,),
)
def event(cls: type[Event]):  # type: ignore
    assert issubclass(cls, Event)
    return dataclass(cls, frozen=True, kw_only=True, slots=True)  # type: ignore
