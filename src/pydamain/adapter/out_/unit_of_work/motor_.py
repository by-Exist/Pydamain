from dataclasses import dataclass, field
from types import TracebackType
from typing import ClassVar, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession  # type: ignore
from motor.core import _MotorTransactionContext  # type: ignore

from ....port.out_.unit_of_work import UnitOfWork


# https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client.html#motor.motor_asyncio.AsyncIOMotorClient.start_session
@dataclass
class BaseMotorUnitOfWork(UnitOfWork):

    CLIENT: ClassVar[AsyncIOMotorClient]

    _session: AsyncIOMotorClientSession = field(init=False)  # type: ignore
    _transaction_context: _MotorTransactionContext = field(init=False)

    async def __aenter__(self):
        self._session = await self.CLIENT.start_session()  # type: ignore
        self._session.start_transaction()  # type: ignore
        await self._transaction_context.__aenter__()  # type: ignore
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        await super().__aexit__(exc_type, exc_value, traceback)
        await self._session.end_session()  # type: ignore

    async def commit(self):
        await super().commit()
        await self._session.commit_transaction()  # type: ignore

    async def rollback(self):
        await super().rollback()
        await self._session.abort_transaction()  # type: ignore
