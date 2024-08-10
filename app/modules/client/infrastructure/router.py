from uuid import UUID
from fastapi import APIRouter, Depends, Response
from app.core.infrastructure.router import BaseRouter
from app.modules.client.application.request.create_params import CreateClientParams
from app.modules.client.infrastructure.service import ClientService, get_client_service

# Requests
from app.modules.client.application.request.create import CreateClientRequest

# Responses
from app.modules.client.application.response.get_many import GetManyClientResponse
from app.modules.client.application.response.get_one import GetOneClientResponse

# Utils
from app.utils.handle_service_result import handle_service_result


class ClientRouter(BaseRouter):

    __prefix__ = "/clients"
    __tag__ = "Clients"

    def __init__(self) -> None:
        super().__init__(APIRouter(prefix=self.__prefix__, tags=[self.__tag__]))

    def _register_routes(self) -> None:
        # Get many clients
        @self._router.get("/", response_model=GetManyClientResponse, status_code=200)
        async def get_many(
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetManyClientResponse:
            result = await service.get_many()

            handle_service_result(result, response)

            return result

        # Get one client
        @self._router.get(
            "/{id_}", response_model=GetOneClientResponse, status_code=200
        )
        async def get_by_id(
            id_: UUID,
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:
            result = await service.get_one(id_)

            handle_service_result(result, response)

            return result

        # Create client (with or without user)
        @self._router.post(
            "/", response_model=GetOneClientResponse, status_code=201
        )
        async def create(
            body: CreateClientRequest,
            params: CreateClientParams = Depends(),
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:
            
            if params.user_dni is not None:
                result = await service.create_without_user(body, params.user_dni)
            else:
                result = await service.create_with_user(body)

            handle_service_result(result, response)

            return result
        

    def get_router(self) -> APIRouter:
        return self._router
