from typing import List
from app.core.application.response.base_response import Response
from app.modules.tank.domain.entity import Tank


class GetManyTankResponse(Response):
    content: List[Tank]
