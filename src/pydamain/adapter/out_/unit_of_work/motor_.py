from dataclasses import dataclass, field
from typing import Any, ClassVar

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession  # type: ignore
from motor.core import _MotorTransactionContext  # type: ignore

from ....port.out_.unit_of_work import UnitOfWork, NotInUOWContextError


# https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client.html#motor.motor_asyncio.AsyncIOMotorClient.start_session
@dataclass
class BaseMotorUnitOfWork(UnitOfWork):

    CLIENT: ClassVar[AsyncIOMotorClient]

    _in_context: bool = field(default=False, init=False)
    _session: AsyncIOMotorClientSession = field(init=False)  # type: ignore
    _transaction_context: _MotorTransactionContext = field(init=False)

    async def __aenter__(self):
        self._in_context = True
        self._session = await self.CLIENT.start_session()  # type: ignore
        return await super().__aenter__()  # return self

    async def __aexit__(self, *args: Any):
        await super().__aexit__(*args)  # call self.rollback
        await self._session.end_session()  # type: ignore
        self._in_context = False

    async def commit(self):
        if not self._in_context:
            raise NotInUOWContextError()
        await self._session.commit_transaction()  # type: ignore

    async def rollback(self):
        if not self._in_context:
            raise NotInUOWContextError()
        await self._session.abort_transaction()  # type: ignore
