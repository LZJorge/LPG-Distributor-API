from app.core.application.response.base_response import Response
from app.modules.tank.domain.entity import Tank


class CreateTankResponse(Response):
    content: Tank | None
