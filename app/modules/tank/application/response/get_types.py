from typing import List
from app.core.application.response.base_response import Response
from app.modules.tank.domain.entity import TankType


class GetTankTypesResponse(Response):
    content: List[TankType]
