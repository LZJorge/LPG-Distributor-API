from app.core.application.response.base_response import Response
from app.modules.user.domain.entity import User


class CreateUserResponse(Response[User]):
    content: User
