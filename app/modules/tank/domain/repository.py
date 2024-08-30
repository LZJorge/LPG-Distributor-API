from abc import ABC, abstractmethod
from app.core.domain.repository import GenericRepository
from app.modules.tank.domain.entity import Tank, TankType


class BaseTankRepository(GenericRepository[Tank], ABC):
    pass


class BaseTankTypeRepository(GenericRepository[TankType], ABC):
    pass
