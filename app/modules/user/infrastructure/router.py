from fastapi import Depends, APIRouter
from app.core.infrastructure.router import BaseRouter

# Requests
from app.modules.user.application.request.create import CreateUserRequest

# Responses
from app.modules.user.application.response.create import CreateUserResponse
from app.modules.user.application.response.get_one import GetOneUserResponse
from app.modules.user.application.response.get_many import GetManyUsersResponse

# Dependencies
from app.modules.user.infrastructure.service import UserService, get_user_service


class UserRouter(BaseRouter):

    __prefix__ = "/users"
    __tag__ = "User"

    def __init__(self) -> None:
        super().__init__(APIRouter(prefix=self.__prefix__, tags=[self.__tag__]))

    def _register_routes(self) -> None:

        @self._router.get("/", response_model=GetManyUsersResponse)
        async def get_all(
            # Query Params
            first_name: str = None,
            last_name: str = None,
            phone: str = None,
            service: UserService = Depends(get_user_service),
        ) -> GetManyUsersResponse:
            query_params: dict = {}

            if first_name:
                query_params["first_name"] = first_name

            if last_name:
                query_params["last_name"] = last_name

            if phone:
                query_params["phone"] = phone

            return await service.get_many(**query_params)

        @self._router.get("/{id_}", response_model=GetOneUserResponse)
        async def get_by_id(
            id_: str, service: UserService = Depends(get_user_service)
        ) -> GetOneUserResponse:
            return await service.get_by_id(id_)

        @self._router.get("/dni/{dni}", response_model=GetOneUserResponse)
        async def get_by_dni(
            dni: str, service: UserService = Depends(get_user_service)
        ) -> GetOneUserResponse:
            return await service.get_by_dni(dni)

        @self._router.put("/{id_}", response_model=CreateUserResponse)
        async def update(
            id_: str,
            body: CreateUserRequest,
            service: UserService = Depends(get_user_service),
        ) -> GetOneUserResponse:
            return await service.update(id_, body)

        @self._router.post("/", response_model=CreateUserResponse, status_code=201)
        async def create(
            body: CreateUserRequest, service: UserService = Depends(get_user_service)
        ) -> CreateUserResponse:
            return await service.create()

    def get_router(self) -> APIRouter:
        return self._router
