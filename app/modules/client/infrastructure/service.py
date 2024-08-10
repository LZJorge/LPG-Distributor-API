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

        client = Client(
            id=ID.generate(),
            user_id=user.id,
            total_orders=0,
        )

        async with self._transaction(user=UserRepository, client=ClientRepository) as t:
            u = await t.user.add(self.__user_mapper.to_model(user))
            c = await t.client.add(self.__mapper.to_model(client))

            c = self.__mapper.to_entity(c)
            c.user = self.__user_mapper.to_entity(u)

        return CreateClientResponse(
            status_code=201,
            success=True,
            message="Client created",
            content=self.__mapper.to_entity(c),
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
            c = await t.client.add(client)
            c.user = user

        return CreateClientResponse(
            status_code=201,
            success=True,
            message="Client created",
            content=self.__mapper.to_entity(c),
        )
    
    # Get
    async def get_one(self, id: str) -> Client:
        async with self._transaction(client=ClientRepository) as t:
                client = await t.client.get(id)
            
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
    async def get_many(self) -> GetManyClientResponse:
        clients = []

        async with self._transaction(client=ClientRepository) as t:
            clients = await t.client.list()

        if len(clients) > 0:
            clients = [self.__mapper.to_entity(client) for client in clients]

        return GetManyClientResponse(
            status_code=200, success=True, message="Clients retrieved", content=clients
        )

def get_client_service(
    transaction: GenericTransaction = Depends(get_transaction),
) -> ClientService:
    return ClientService(transaction)