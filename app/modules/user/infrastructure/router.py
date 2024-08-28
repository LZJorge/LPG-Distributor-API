from uuid import UUID
from fastapi import Depends, APIRouter, Query, Response
from app.core.infrastructure.router import BaseRouter

# Requests
from app.modules.user.application.request.create import CreateUserRequest
from app.modules.user.application.request.list_params import ListUsersParams

# Responses
from app.modules.user.application.response.create import CreateUserResponse
from app.modules.user.application.response.get_one import GetOneUserResponse
from app.modules.user.application.response.get_many import GetManyUsersResponse
from app.modules.user.application.response.update import UpdateUserResponse

# Dependencies
from app.modules.user.infrastructure.service import UserService, get_user_service
from app.utils.handle_service_result import handle_service_result


class UserRouter(BaseRouter):

    __prefix__ = "/users"
    __tag__ = "User"

    def __init__(self) -> None:
        super().__init__(APIRouter(prefix=self.__prefix__, tags=[self.__tag__]))

    def _register_routes(self) -> None:

        @self._router.get("/", response_model=GetManyUsersResponse, status_code=200)
        async def get_many(
            offset: int = 0,
            limit: int = Query(default=100, le=100),
            params: ListUsersParams = Depends(),
            service: UserService = Depends(get_user_service),
            response: Response = Response(),
        ) -> GetManyUsersResponse:
            query_params: dict = {
                key: value for key, value in params if value is not None
            }

            result = await service.get_many(offset, limit, **query_params)

            handle_service_result(result, response)

            return result

        @self._router.get("/{_id}", response_model=GetOneUserResponse, status_code=200)
        async def get_by_id(
            _id: UUID,
            service: UserService = Depends(get_user_service),
            response: Response = Response(),
        ) -> GetOneUserResponse:
            result = await service.get_one(_id)

            handle_service_result(result, response)

            return result

        @self._router.get(
            "/dni/{dni}", response_model=GetOneUserResponse, status_code=200
        )
        async def get_by_dni(
            dni: str,
            service: UserService = Depends(get_user_service),
            response: Response = Response(),
        ) -> GetOneUserResponse:
            result = await service.get_one_by_dni(dni)

            handle_service_result(result, response)

            return result

        @self._router.put("/{_id}", response_model=UpdateUserResponse, status_code=200)
        async def update(
            _id: UUID,
            body: CreateUserRequest,
            service: UserService = Depends(get_user_service),
            response: Response = Response(),
        ) -> UpdateUserResponse:
            result = await service.update(_id, body)

            handle_service_result(result, response)

            return result

        @self._router.post("/", response_model=CreateUserResponse, status_code=201)
        async def create(
            body: CreateUserRequest,
            service: UserService = Depends(get_user_service),
            response: Response = Response(),
        ) -> CreateUserResponse:
            result = await service.create(body)

            handle_service_result(result, response)

            return result

    def get_router(self) -> APIRouter:
        return self._router
