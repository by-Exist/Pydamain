import asyncio
from typing import Any, Iterable, TypeVar

from ..messages.main import (
    Command,
    CommandHandler,
    Event,
    EventHandler,
    events_context_var,
)


# ============================================================================
# Event Catch Context
# ============================================================================
class EventCatchContext:

    __slots__ = ("_results", "_token")

    @property
    def events(self):
        return self._results

    def __enter__(self):
        self._token = events_context_var.set([])
        return self

    def __exit__(self, *args: tuple[Any]):
        self._results = events_context_var.get()
        events_context_var.reset(self._token)


# ============================================================================
# Domain Application
# ============================================================================
C = TypeVar("C", bound=Command)
E = TypeVar("E", bound=Event)
R = TypeVar("R")


class DomainApplication:
    def __init__(
        self,
        *,
        cmd_deps: dict[str, Any],
        evt_deps: dict[str, Any],
    ) -> None:
        self._cmd_deps: dict[str, Any] = cmd_deps
        self._evt_deps: dict[str, Any] = evt_deps

    async def pre_cmd_handle(self, cmd: C, handler: CommandHandler[C]):
        ...

    async def post_cmd_handle(self, cmd: C, handler: CommandHandler[C]):
        ...

    async def pre_evt_handle(self, evt: E, handler: EventHandler[E]):
        ...

    async def post_evt_handle(self, evt: E, handler: EventHandler[E]):
        ...

    async def handle(self, cmd: Command):
        result, events = await self._handle_cmd_with_task(cmd)
        await self._handle_evts(events)
        return result

    async def _handle_cmd_with_task(self, cmd: Command) -> tuple[Any, list[Event]]:
        handler = type(cmd).handler
        if not handler:
            return None, []
        return await asyncio.create_task(
            self._handle_cmd_with_event_catch_context(cmd, handler)
        )

    async def _handle_cmd_with_event_catch_context(
        self, cmd: C, handler: CommandHandler[C]
    ):
        with EventCatchContext() as event_catcher:
            await self.pre_cmd_handle(cmd, handler)
            result = await handler(cmd, **self._cmd_deps)
            await self.post_cmd_handle(cmd, handler)
        return result, event_catcher.events

    async def _handle_evts(self, evts: Iterable[Event]):
        coros = (self._handle_evt(evt) for evt in evts)
        await asyncio.gather(*coros, return_exceptions=False)

    async def _handle_evt(self, evt: Event):
        handlers = type(evt).handlers
        if not handlers:
            return
        coros = (self._handle_evt_once(evt, handler) for handler in handlers)
        await asyncio.gather(*coros, return_exceptions=False)

    async def _handle_evt_once(self, evt: E, handler: EventHandler[E]):
        await self.pre_evt_handle(evt, handler)
        await handler(evt, **self._evt_deps)
        await self.post_evt_handle(evt, handler)
