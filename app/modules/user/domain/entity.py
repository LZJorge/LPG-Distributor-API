from dataclasses import dataclass
from app.core.domain.entity import Entity


@dataclass
class User(Entity):
    dni: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
