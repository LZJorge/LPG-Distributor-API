from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from app.config.database import Base
from app.core.domain.entity import Entity

E = TypeVar("E", bound=Entity)
M = TypeVar("M", bound=Base)


class GenericMapper(Generic[E, M], ABC):

    @abstractmethod
    def to_model(self, entity: E) -> M:
        raise NotImplementedError

    @abstractmethod
    def to_entity(self, model: M) -> E:
        raise NotImplementedError
