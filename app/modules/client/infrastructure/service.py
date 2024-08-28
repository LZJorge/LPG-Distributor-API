from fastapi import Depends
from app.modules.user.domain.entity import User
from app.modules.client.domain.entity import Client
from app.core.domain.transaction import GenericTransaction
from app.core.infrastructure.transaction import get_transaction
from app.modules.client.infrastructure.mapper import ClientMapper
from app.core.domain.id import ID

# Requests
from app.modules.client.application.request.create import CreateClientRequest

# Responses
from app.modules.client.application.response.create import CreateClientResponse
from app.modules.client.application.response.get_one import GetOneClientResponse
from app.modules.client.application.response.get_many import GetManyClientResponse

# Repositories
from app.modules.user.infrastructure.mapper import UserMapper
from app.modules.user.infrastructure.repository import UserRepository
from app.modules.client.infrastructure.repository import ClientRepository


class ClientService:
    __mapper: ClientMapper = ClientMapper()
    __user_mapper: UserMapper = UserMapper()

    def __init__(
        self, transaction: GenericTransaction = Depends(get_transaction)
    ) -> None:
        self._transaction = transaction

    # Create
    async def create_with_user(self, dto: CreateClientRequest) -> CreateClientResponse:
        user = User(
            id=ID.generate(),
            dni=dto.user.dni,
            first_name=dto.user.first_name,
            last_name=dto.user.last_name,
            email=dto.user.email,
            phone=dto.user.phone,
            address=dto.user.address,
        )

        client = Client(id=ID.generate(), user_id=user.id)

        async with self._transaction(user=UserRepository) as t:
            user_exists = await t.user.get_by_dni(user.dni)

        if user_exists:
            return CreateClientResponse(
                status_code=409,
                success=False,
                message=f"User by dni {user.dni} already exists",
                content=None,
            )

        async with self._transaction(user=UserRepository, client=ClientRepository) as t:
            await t.user.add(self.__user_mapper.to_model(user))
            await t.client.add(self.__mapper.to_model(client))

        client.user = user

        return CreateClientResponse(
            status_code=201,
            success=True,
            message="Client created",
            content=client,
        )

    async def create_without_user(self, user_dni: str) -> CreateClientResponse:
        async with self._transaction(user=UserRepository) as t:
            user = await t.user.get_by_dni(user_dni)

        if not user:
            return CreateClientResponse(
                status_code=404,
                success=False,
                message=f"User by dni: {user_dni} not found",
                content=None,
            )

        client = Client(
            id=ID.generate(),
            user_id=user.id,
        )

        async with self._transaction(client=ClientRepository) as t:
            client_exists = await t.client.get_by_user_id(user.id)

        if client_exists:
            return CreateClientResponse(
                status_code=409,
                success=False,
                message=f"Client by dni: {user_dni} already exists",
                content=None,
            )

        async with self._transaction(client=ClientRepository) as t:
            await t.client.add(self.__mapper.to_model(client))

        client.user = self.__user_mapper.to_entity(user)

        return CreateClientResponse(
            status_code=201,
            success=True,
            message="Client created",
            content=client,
        )

    # Get
    async def get_one(self, _id: str) -> Client:
        async with self._transaction(client=ClientRepository) as t:
            client = await t.client.get(_id)

        if not client:
            return GetOneClientResponse(
                status_code=404, success=False, message="Client not found", content=None
            )

        return GetOneClientResponse(
            status_code=200,
            success=True,
            message="Client retrieved",
            content=self.__mapper.to_entity(client),
        )

    # Get one by user dni
    async def get_by_user_dni(self, user_dni: str) -> GetOneClientResponse:
        async with self._transaction(client=ClientRepository) as t:
            client = await t.client.get_by_dni(user_dni)

        if not client:
            return GetOneClientResponse(
                status_code=404, success=False, message="Client not found", content=None
            )

        return GetOneClientResponse(
            status_code=200,
            success=True,
            message="Client retrieved",
            content=self.__mapper.to_entity(client),
        )

    async def get_by_user_id(self, user_id: str) -> GetOneClientResponse:
        async with self._transaction(client=ClientRepository) as t:
            client = await t.client.get_by_user_id(user_id)

        if not client:
            return GetOneClientResponse(
                status_code=404, success=False, message="Client not found", content=None
            )

        return GetOneClientResponse(
            status_code=200,
            success=True,
            message="Client retrieved",
            content=self.__mapper.to_entity(client),
        )

    # List
    async def get_many(self, offset: int, limit: int) -> GetManyClientResponse:
        clients = []

        async with self._transaction(client=ClientRepository) as t:
            clients = await t.client.list(offset, limit)

        if len(clients) > 0:
            clients = [self.__mapper.to_entity_with_user(client) for client in clients]

        return GetManyClientResponse(
            status_code=200, success=True, message="Clients retrieved", content=clients
        )


def get_client_service(
    transaction: GenericTransaction = Depends(get_transaction),
) -> ClientService:
    return ClientService(transaction)
