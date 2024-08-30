from app.core.infrastructure.mapper import GenericMapper
from app.modules.client.domain.entity import Client
from app.modules.client.infrastructure.model import ClientModel
from app.modules.user.domain.entity import User


class ClientMapper(GenericMapper[Client, ClientModel]):
    def to_entity(self, model: ClientModel) -> Client:
        return Client(
            id=model.id,
            total_orders=model.total_orders,
            created_at=model.created_at,
            user_id=model.user_id,
        )

    def to_model(self, entity: Client) -> ClientModel:
        return ClientModel(
            id=entity.id,
            total_orders=entity.total_orders,
            created_at=entity.created_at,
            user_id=entity.user_id,
        )

    def to_entity_with_user(self, model: ClientModel) -> Client:
        return Client(
            id=model.id,
            total_orders=model.total_orders,
            created_at=model.created_at,
            user_id=model.user_id,
            user=User(
                id=model.user.id,
                dni=model.user.dni,
                first_name=model.user.first_name,
                last_name=model.user.last_name,
                email=model.user.email,
                phone=model.user.phone,
                address=model.user.address,
            ),
        )
