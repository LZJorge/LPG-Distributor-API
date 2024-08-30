from datetime import date
from sqlalchemy import Boolean, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from app.modules.client.infrastructure.model import ClientModel


class TankTypeModel(Base):
    __tablename__ = "tank_types"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(64))
    price: Mapped[float] = mapped_column(Float)
    capacity: Mapped[int] = mapped_column(Integer)


class TankModel(Base):
    __tablename__ = "tanks"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True)
    type_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tank_types.id")
    )
    client_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"))
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[date] = mapped_column(String, default=date.today())

    type: Mapped["TankTypeModel"] = relationship(
        "TankTypeModel", backref="tank", single_parent=True, lazy="joined"
    )

    client: Mapped["ClientModel"] = relationship(
        "ClientModel", backref="tank", single_parent=True, lazy="joined"
    )
