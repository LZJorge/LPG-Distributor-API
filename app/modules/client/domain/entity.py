from typing import Optional
from datetime import date
from dataclasses import dataclass
from uuid import UUID
from app.core.domain.entity import Entity
from app.modules.user.domain.entity import User


@dataclass
class Client(Entity):
    user_id: UUID
    total_orders: int = 0
    created_at: str = date.today()
    user: Optional[User] = None