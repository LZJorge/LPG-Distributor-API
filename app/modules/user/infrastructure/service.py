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
from app.modules.user.application.response.update import UpdateUserResponse

# Entities
from app.modules.user.domain.entity import User

# Repositories
from app.modules.user.infrastructure.repository import UserRepository


class UserService:
    __mapper = UserMapper()

    def __init__(
        self, transaction: GenericTransaction = Depends(get_transaction)
    ) -> None:
        self._transaction = transaction

    # Use cases
    async def create(self, dto: CreateUserRequest) -> CreateUserResponse:
        try:
            async with self._transaction(user=UserRepository) as t:
                user_exists = await t.user.get_by_dni(dto.dni)
        except Exception:
            return CreateUserResponse(
                status_code=500, success=False, message="Unexpected error", content=None
            )

        if user_exists:
            return CreateUserResponse(
                status_code=409,
                success=False,
                message=f"User by dni {dto.dni} already exists",
                content=None,
            )

        user = User(
            id=ID.generate(),
            dni=dto.dni,
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            phone=dto.phone,
            address=dto.address,
        )

        try:
            async with self._transaction(user=UserRepository) as t:
                u = await t.user.add(self.__mapper.to_model(user))
        except Exception:
            return CreateUserResponse(
                status_code=500, success=False, message="Unexpected error", content=None
            )

        return CreateUserResponse(
            status_code=201,
            success=True,
            message="User created",
            content=self.__mapper.to_entity(u),
        )

    async def get_one(self, id: str) -> GetOneUserResponse:
        async with self._transaction(user=UserRepository) as t:
            user = await t.user.get(id)

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

    async def get_one_by_dni(self, dni: str) -> GetOneUserResponse:
        async with self._transaction(user=UserRepository) as t:
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

    async def get_many(
        self, offset: int, limit: int, **filters
    ) -> GetManyUsersResponse:
        users = []

        async with self._transaction(user=UserRepository) as t:
            query = await t.user.list(offset, limit, **filters)

        if len(query) > 0:
            users = [self.__mapper.to_entity(user) for user in query]

        return GetManyUsersResponse(
            status_code=200, success=True, message="Users retrieved", content=users
        )

    async def update(self, dni: str, dto: CreateUserRequest) -> User:
        async with self._transaction(user=UserRepository) as t:
            user = await t.user.get(dni)

            if not user:
                return UpdateUserResponse(
                    status_code=404,
                    success=False,
                    message="User not found",
                    content=None,
                )

            for k, v in vars(dto).items():
                setattr(user, k, v)

            await t.user.update(user)

        return UpdateUserResponse(
            status_code=200,
            success=True,
            message="User updated",
            content=self.__mapper.to_entity(user),
        )


def get_user_service(
    transaction: GenericTransaction = Depends(get_transaction),
) -> UserService:
    return UserService(transaction)
