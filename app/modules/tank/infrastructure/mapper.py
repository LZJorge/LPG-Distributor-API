from app.core.infrastructure.mapper import GenericMapper
from app.modules.tank.domain.entity import Tank, TankType
from app.modules.tank.infrastructure.model import TankModel, TankTypeModel


class TankMapper(GenericMapper[Tank, TankModel]):
    def to_entity(self, model: TankModel) -> Tank:
        return Tank(
            id=model.id,
            type_id=model.type_id,
            client_id=model.client_id,
            delivered=model.delivered,
            created_at=model.created_at,
            type=self.type_to_entity(model.type),
        )

    def to_model(self, entity: Tank) -> TankModel:
        return TankModel(
            id=entity.id,
            type_id=entity.type_id,
            client_id=entity.client_id,
            delivered=entity.delivered,
            created_at=entity.created_at,
        )

    def type_to_entity(self, model: TankTypeModel) -> Tank:
        return TankType(
            id=model.id, name=model.name, price=model.price, capacity=model.capacity
        )
