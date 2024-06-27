from app.core.application.response.base_response import Response
from app.modules.user.domain.entity import User


class GetOneUserResponse(Response[User]):
    content: User | None
