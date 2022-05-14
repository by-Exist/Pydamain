import asyncio
from typing import Any, Iterable, Literal, TypeVar, overload

from ..messages import Command, Event
from ..messages.base import Message, MessageCatchContext

from .handler import Handler


C = TypeVar("C", bound=Command)
E = TypeVar("E", bound=Event)

CommandHandler = Handler[C, Any]
EventHandler = Handler[E, Any]
EventHandlers = Iterable[EventHandler[E]]


class MessageBus:
    def __init__(
        self,
        *,
        command_deps: dict[str, Any],
        event_deps: dict[str, Any],
    ) -> None:
        self._command_deps: dict[str, Any] = command_deps
        self._event_deps: dict[str, Any] = event_deps
        self._command_handler_map: dict[type[Command], CommandHandler[Any]] = {}
        self._event_handler_map: dict[type[Event], EventHandlers[Any]] = {}

    def register_command(self, command_type: type[C], handler: CommandHandler[C]):
        self._command_handler_map[command_type] = handler

    def register_event(self, event_type: type[E], handlers: EventHandlers[E]):
        self._event_handler_map[event_type] = handlers

    @overload
    async def dispatch(
        self, message: Message, return_hooked_task: Literal[False] = False
    ) -> Any:
        ...

    @overload
    async def dispatch(
        self, message: Message, return_hooked_task: Literal[True] = True
    ) -> tuple[Any, asyncio.Future[list[Any]]]:
        ...

    async def dispatch(self, message: Message, return_hooked_task: bool = False):
        result, hooked = await asyncio.create_task(self._handle(message))
        coros = (self._handle(msg) for msg in hooked)
        hooked_task = asyncio.gather(*coros, return_exceptions=True)
        if return_hooked_task:
            return result, hooked_task
        await hooked_task
        return result

    async def _handle(self, message: Message):
        with MessageCatchContext() as message_catcher:
            if isinstance(message, Command):
                result = await self._handle_command(message)
            elif isinstance(message, Event):
                result = await self._handle_event(message)
            else:
                raise RuntimeError("message must be a command or an event.")
        return result, message_catcher.messages

    async def _handle_command(self, command: Command):
        handler = self._command_handler_map[type(command)]
        await self._pre_handle_command(command, handler)
        result = await handler(command, **self._command_deps)
        await self._post_handle_command(command, handler)
        return result

    async def _handle_event(self, event: Event):
        handlers = self._event_handler_map[type(event)]
        coros = (self.__handle_event(event, handler) for handler in handlers)
        return await asyncio.gather(*coros, return_exceptions=True)

    async def __handle_event(self, event: E, handler: EventHandler[E]):
        await self._pre_handle_event(event, handler)
        result = await handler(event, **self._event_deps)
        await self._post_handle_event(event, handler)
        return result

    async def _pre_handle_command(self, command: C, handler: CommandHandler[C]):
        ...

    async def _post_handle_command(self, command: C, handler: CommandHandler[C]):
        ...

    async def _pre_handle_event(self, event: E, handler: EventHandler[E]):
        ...

    async def _post_handle_event(self, event: E, handler: EventHandler[E]):
        ...
