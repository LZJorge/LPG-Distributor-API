from datetime import date
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from app.modules.user.infrastructure.model import UserModel


class ClientModel(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True)
    created_at: Mapped[date] = mapped_column(String, default=date.today())
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    user: Mapped["UserModel"] = relationship(
        "UserModel", backref="client", single_parent=True, lazy="joined"
    )
