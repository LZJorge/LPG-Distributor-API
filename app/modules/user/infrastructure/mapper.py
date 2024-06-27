from app.core.infrastructure.mapper import GenericMapper
from app.modules.user.domain.entity import User
from app.modules.user.infrastructure.model import UserModel


class UserMapper(GenericMapper[User, UserModel]):

    def to_entity(cls, model: UserModel) -> User:
        return User(
            id=model.id,
            dni=model.dni,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone=model.phone,
            address=model.address,
        )

    def to_model(cls, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            dni=entity.dni,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone=entity.phone,
            address=entity.address,
        )
