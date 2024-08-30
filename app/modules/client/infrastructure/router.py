from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response
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
            offset: int = 0,
            limit: int = Query(default=100, le=100),
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetManyClientResponse:
            result = await service.get_many(offset, limit)

            handle_service_result(result, response)

            return result

        # Get one client
        @self._router.get(
            "/{_id}", response_model=GetOneClientResponse, status_code=200
        )
        async def get_by_id(
            _id: UUID,
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:
            result = await service.get_one(_id)

            handle_service_result(result, response)

            return result

        # Get one client by user dni
        @self._router.get(
            "/user/dni/{user_dni}", response_model=GetOneClientResponse, status_code=200
        )
        async def get_by_dni(
            user_dni: str,
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:
            result = await service.get_by_user_dni(user_dni)

            handle_service_result(result, response)

            return result

        # Get one client by user id
        @self._router.get(
            "/user/id/{user_id}", response_model=GetOneClientResponse, status_code=200
        )
        async def get_by_user_id(
            user_id: UUID,
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:
            result = await service.get_by_user_id(user_id)

            handle_service_result(result, response)

            return result

        # Create client with is user (unregistered user)
        @self._router.post("/", response_model=GetOneClientResponse, status_code=201)
        async def create_with_user(
            body: CreateClientRequest,
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:

            result = await service.create_with_user(body)

            handle_service_result(result, response)

            return result

        # Create client without user (already registered)
        @self._router.post(
            "/{user_dni}", response_model=GetOneClientResponse, status_code=201
        )
        async def create_without_user(
            params: CreateClientParams = Depends(),
            service: ClientService = Depends(get_client_service),
            response: Response = Response(),
        ) -> GetOneClientResponse:

            result = await service.create_without_user(params.user_dni)

            handle_service_result(result, response)

            return result
