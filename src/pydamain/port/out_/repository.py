from __future__ import annotations

from typing import Generic, TypeVar

from abc import ABCMeta, abstractmethod


Aggregate = TypeVar("Aggregate")
AggregateIdentity = TypeVar("AggregateIdentity")


class AbstractCollectionRepository(
    Generic[Aggregate, AggregateIdentity], metaclass=ABCMeta
):
    @abstractmethod
    def add(self, _aggregate: Aggregate):
        ...

    @abstractmethod
    async def get(self, _identity: AggregateIdentity) -> Aggregate | None:
        ...


class AbstractPersistenceRepository(
    Generic[Aggregate, AggregateIdentity], metaclass=ABCMeta
):
    @abstractmethod
    async def save(self, _aggregate: Aggregate):
        ...

    @abstractmethod
    async def get(self, _identity: AggregateIdentity) -> Aggregate | None:
        ...
