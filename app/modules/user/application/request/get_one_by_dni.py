from pydantic import field_validator
from app.core.application.request.base_request import Request
from app.modules.user.domain.value_objects.dni import DNI


class GetOneByDniRequest(Request):
    dni: str

    @classmethod
    @field_validator("dni")
    def validate_dni(cls, v):
        return DNI(v)
