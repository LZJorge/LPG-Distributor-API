from typing import List
from app.core.application.response.base_response import Response
from app.modules.client.domain.entity import Client


class GetManyClientResponse(Response):
    content: List[Client]