from __future__ import annotations

from typing import Generic, TypeVar

from abc import ABCMeta, abstractmethod
from uuid import UUID


A = TypeVar("A")


class AbstractRepository(Generic[A], metaclass=ABCMeta):
    @abstractmethod
    def add(self, aggregate: A):
        ...

    @abstractmethod
    async def get(self, identity: UUID) -> A | None:
        ...
