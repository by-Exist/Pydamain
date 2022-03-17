from typing import Any, Callable, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from pydamain.domain import Aggregate
from pydamain.port.out_.repository import AbstractRepository


A = TypeVar("A", bound=Aggregate)


class BaseSQLAlchemyRepository(AbstractRepository[A]):

    session_factory: Callable[[], AsyncSession]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "session_factory"):
            raise TypeError(f"'session_factory' not set to {cls.__name__}.")

    def __init__(self, aggregate_cls: type[A]):
        self._aggregate_cls = aggregate_cls

    async def __aenter__(self):
        self.session = self.session_factory()
        return self

    async def __aexit__(self, *args: tuple[Any]):
        await self.session.rollback()
        await self.session.close()

    def add(self, aggregate: A):
        self.session.add(aggregate)

    async def get(self, identity: UUID) -> A | None:
        return await self.session.get(self._aggregate_cls, identity)

    async def commit(self):
        await self.session.commit()
