from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from app.core.domain.entity import Entity

T = TypeVar("T", bound=Entity)


class GenericRepository(Generic[T], ABC):

    @abstractmethod
    async def get(self, id_: str) -> T:
        raise NotImplementedError

    @abstractmethod
    async def list(self, **filters) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, record: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(self, record: T) -> None:
        raise NotImplementedError
