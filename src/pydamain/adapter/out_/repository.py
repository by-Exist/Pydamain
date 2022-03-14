from typing import Any, Callable, TypeVar
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from pydamain.domain.model import Aggregate
from pydamain.port.out_.repository import AbstractRepository


A = TypeVar("A", bound=Aggregate)


class BaseSQLModelRepository(AbstractRepository[A]):

    session_factory: Callable[[], AsyncSession]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "session_factory"):
            raise TypeError(f"'session_factory' not set to {cls.__name__}.")

    def __init__(self, aggregate_cls: type[A]):
        self._aggregate_cls = aggregate_cls

    async def __aenter__(self):
        self._session = self.session_factory()
        return self

    async def __aexit__(self, *args: tuple[Any]):
        await self._session.rollback()
        await self._session.close()

    def add(self, aggregate: A):
        self._session.add(aggregate)

    async def get(self, identity: UUID) -> A | None:
        return await self._session.get(self._aggregate_cls, identity)

    async def commit(self):
        await self._session.commit()
