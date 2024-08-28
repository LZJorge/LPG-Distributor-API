from app.core.application.request.base_request import Request
from app.modules.user.application.request.create import CreateUserRequest


class CreateClientRequest(Request):
    user: CreateUserRequest
