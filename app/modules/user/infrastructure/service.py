from fastapi import Depends
from app.core.domain.transaction import GenericTransaction
from app.core.infrastructure.transaction import get_transaction
from app.core.domain.id import ID

# Mapper
from app.modules.user.infrastructure.mapper import UserMapper

# Requests
from app.modules.user.application.request.create import CreateUserRequest

# Responses
from app.modules.user.application.response.create import CreateUserResponse
from app.modules.user.application.response.get_one import GetOneUserResponse
from app.modules.user.application.response.get_many import GetManyUsersResponse

from app.modules.user.domain.entity import User


class UserService:
    __mapper = UserMapper()

    def __init__(
        self, transaction: GenericTransaction = Depends(get_transaction)
    ) -> None:
        self._transaction = transaction

    # Use cases
    async def create(self, dto: CreateUserRequest) -> CreateUserResponse:
        user = User(
            id=ID.generate(),
            dni=dto.dni,
            firstname=dto.firstname,
            lastname=dto.lastname,
            email=dto.email,
            phone=dto.phone,
        )

        async with self._transaction as t:
            t.user.add(user)

            await t.commit()

        return CreateUserResponse(
            status_code=201, success=True, message="User created", content=user
        )

    async def get_one(self, id: str) -> GetOneUserResponse:
        async with self._transaction as t:
            user = await t.user.get_one(id)

        return GetOneUserResponse(
            status_code=200,
            success=True,
            message="User retrieved",
            content=self.__mapper.to_entity(user),
        )

    async def get_by_dni(self, dni: str) -> GetOneUserResponse:
        async with self._transaction() as t:
            user = await t.user.get_by_dni(dni)

        if not user:
            return GetOneUserResponse(
                status_code=404, success=False, message="User not found", content=None
            )

        return GetOneUserResponse(
            status_code=200,
            success=True,
            message="User retrieved",
            content=self.__mapper.to_entity(user),
        )

    async def get_many(self, **filters) -> GetManyUsersResponse:
        users = []

        async with self._transaction() as t:
            query = await t.user.list(**filters)

        if len(query) > 0:
            users = [self.__mapper.to_entity(user) for user in query]

        return GetManyUsersResponse(
            status_code=200, success=True, message="Users retrieved", content=users
        )

    async def update(self, dni: str, dto: CreateUserRequest) -> User:
        async with self._transaction as t:
            user = await t.user.get_one(dni)

            for k, v in vars(dto).items():
                setattr(user, k, v)

            t.user.update(user)

        return user


def get_user_service(
    transaction: GenericTransaction = Depends(get_transaction),
) -> UserService:
    return UserService(transaction)
