from uuid import UUID
from fastapi import Depends
from app.core.domain.id import ID
from app.core.domain.transaction import GenericTransaction
from app.core.infrastructure.transaction import get_transaction

# Mapper
from app.modules.client.infrastructure.mapper import ClientMapper
from app.modules.tank.infrastructure.mapper import TankMapper

# Requests

# Responses
from app.modules.tank.application.response.create import CreateTankResponse
from app.modules.tank.application.response.get_one import GetOneTankResponse
from app.modules.tank.application.response.get_many import GetManyTankResponse
from app.modules.tank.application.response.get_types import GetTankTypesResponse

# Entities
from app.modules.tank.domain.entity import Tank

# Repositories
from app.modules.tank.infrastructure.repository import (
    TankRepository,
    TankTypesRepository,
)
from app.modules.client.infrastructure.repository import ClientRepository


class TankService:
    __mapper = TankMapper()
    __client_mapper = ClientMapper()

    def __init__(
        self, transaction: GenericTransaction = Depends(get_transaction)
    ) -> None:
        self._transaction = transaction

    # Create Gas Tank
    async def create(self, type_id: UUID, client_dni: str) -> None:
        async with self._transaction(tank_types=TankTypesRepository) as t:
            tank_type = await t.tank_types.get(type_id)

        if not tank_type:
            return CreateTankResponse(
                status_code=404,
                success=False,
                message="Tank type not found",
                content=None,
            )

        async with self._transaction(client=ClientRepository) as t:
            client = await t.client.get_by_dni(client_dni)

        if not client:
            return CreateTankResponse(
                status_code=404, success=False, message="Client not found", content=None
            )

        tank = Tank(id=ID.generate(), type_id=type_id, client_id=client.id)

        client.total_orders += 1

        async with self._transaction(tank=TankRepository, client=ClientRepository) as t:
            await t.tank.add(self.__mapper.to_model(tank))
            await t.client.update(client)

        tank.type = self.__mapper.type_to_entity(tank_type)
        tank.client = self.__client_mapper.to_entity_with_user(client)

        return CreateTankResponse(
            status_code=201,
            success=True,
            message=f"Tank for client {tank.client.user.first_name} - {client_dni} created",
            content=tank,
        )

    # Get Gas Tank Types
    async def get_types(self) -> GetTankTypesResponse:
        async with self._transaction(tank_types=TankTypesRepository) as t:
            types = await t.tank_types.list(0, 100)

        if len(types) > 0:
            types = [self.__mapper.type_to_entity(t) for t in types]

        return GetTankTypesResponse(
            status_code=200,
            success=True,
            message="Gas Tank Types retrieved",
            content=types,
        )

    # Get Gas Tank
    async def get_one(self, _id: UUID) -> GetOneTankResponse:
        async with self._transaction(tank=TankRepository) as t:
            tank = await t.tank.get(_id)

        if not tank:
            return GetOneTankResponse(
                status_code=404,
                success=False,
                message="Gas tank not found",
                content=None,
            )

        return GetOneTankResponse(
            status_code=200,
            success=True,
            message="Tank retrieved",
            content=self.__mapper.to_entity(tank),
        )

    # Get many Gas Tanks
    async def get_many(self, offset: int, limit: int, **filters) -> GetOneTankResponse:
        tanks = []

        async with self._transaction(tank=TankRepository) as t:
            tanks = await t.tank.list(offset, limit, **filters)

        if len(tanks) > 0:
            tanks = [self.__mapper.to_entity(tank) for tank in tanks]

        return GetManyTankResponse(
            status_code=200, success=True, message="Gas Tanks retrieved", content=tanks
        )

    # Update gas tank status
    async def update(self, _id: UUID) -> GetOneTankResponse:
        # get tank
        async with self._transaction(tank=TankRepository) as t:
            tank = await t.tank.get(_id)

        if not tank:
            GetOneTankResponse(
                status_code=404,
                success=False,
                message="Gas tank not found",
                content=None,
            )

        if tank.delivered:
            return GetOneTankResponse(
                status_code=409,
                success=False,
                message="Tank already delivered",
                content=None,
            )

        tank.delivered = True

        async with self._transaction(tank=TankRepository) as t:
            await t.tank.update(tank)

        return GetOneTankResponse(
            status_code=200,
            success=True,
            message="Tank delivered",
            content=self.__mapper.to_entity(tank),
        )


def get_tank_service(
    transaction: GenericTransaction = Depends(get_transaction),
) -> TankService:
    return TankService(transaction)
