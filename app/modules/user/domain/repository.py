from abc import ABC, abstractmethod
from app.core.domain.repository import GenericRepository
from app.modules.user.domain.entity import User
from app.modules.user.domain.value_objects.dni import DNI


class BaseUserRepository(GenericRepository[User], ABC):

    @abstractmethod
    async def get_by_dni(self, dni: DNI) -> User:
        raise NotImplementedError
