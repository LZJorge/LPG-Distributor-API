from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response
from app.core.infrastructure.router import BaseRouter

# Requests
from app.modules.tank.application.request.create_params import CreateTankParams

# Responses
from app.modules.tank.application.request.get_many_params import GetManyTanksParams
from app.modules.tank.application.response.create import CreateTankResponse
from app.modules.tank.application.response.get_one import GetOneTankResponse
from app.modules.tank.application.response.get_many import GetManyTankResponse
from app.modules.tank.application.response.get_types import GetTankTypesResponse

# Service
from app.modules.tank.infrastructure.service import TankService, get_tank_service

# Utils
from app.utils.handle_service_result import handle_service_result


class TankRouter(BaseRouter):

    __prefix__ = "/tanks"
    __tag__ = "Tank"

    def __init__(self) -> None:
        super().__init__(APIRouter(prefix=self.__prefix__, tags=[self.__tag__]))

    def _register_routes(self) -> None:

        @self._router.get("/types")
        async def get_types(
            service: TankService = Depends(get_tank_service),
            response: Response = Response(),
        ) -> GetTankTypesResponse:
            result = await service.get_types()

            handle_service_result(result, response)

            return result

        @self._router.get("/")
        async def get_many(
            offset: int = 0,
            limit: int = Query(default=100, le=100),
            params: GetManyTanksParams = Depends(),
            service: TankService = Depends(get_tank_service),
            response: Response = Response(),
        ) -> GetManyTankResponse:
            query_params: dict = {
                key: value for key, value in params if value is not None
            }

            result = await service.get_many(offset, limit, **query_params)

            handle_service_result(result, response)

            return result

        @self._router.get("/{tank_id}")
        async def get_by_id(
            tank_id: UUID,
            service: TankService = Depends(get_tank_service),
            response: Response = Response(),
        ) -> GetOneTankResponse:
            result = await service.get_one(tank_id)

            handle_service_result(result, response)

            return result

        @self._router.post("/")
        async def create(
            params: CreateTankParams = Depends(),
            service: TankService = Depends(get_tank_service),
            response: Response = Response(),
        ) -> CreateTankResponse:
            result = await service.create(
                type_id=params.type_id, client_dni=params.client_dni
            )

            handle_service_result(result, response)

            return result

        @self._router.put("/{tank_id}")
        async def update(
            tank_id: UUID,
            service: TankService = Depends(get_tank_service),
            response: Response = Response(),
        ) -> GetOneTankResponse:
            result = await service.update(tank_id)

            handle_service_result(result, response)

            return result
