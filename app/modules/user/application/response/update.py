from app.core.application.response.base_response import Response
from app.modules.user.domain.entity import User


class UpdateUserResponse(Response[User]):
    content: User | None
