from abc import ABC, abstractmethod
from app.core.domain.repository import GenericRepository
from app.modules.client.domain.entity import Client


class BaseClientRepository(GenericRepository[Client], ABC):

    @abstractmethod
    async def get_by_dni(self, dni: str) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, id_: str) -> Client:
        raise NotImplementedError
