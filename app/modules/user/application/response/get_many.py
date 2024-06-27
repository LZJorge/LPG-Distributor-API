from typing import List
from app.core.application.response.base_response import Response
from app.modules.user.domain.entity import User


class GetManyUsersResponse(Response[User]):
    content: List[User]
