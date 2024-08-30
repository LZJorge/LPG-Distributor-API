from datetime import date
from typing import Optional
from uuid import UUID
from dataclasses import dataclass
from app.core.domain.entity import Entity


@dataclass
class TankType(Entity):
    name: str
    price: float
    capacity: int


@dataclass
class Tank(Entity):
    type_id: UUID
    client_id: UUID
    delivered: bool = False
    created_at: str = date.today()
    type: Optional[TankType] = None
