from uuid import UUID

from pydantic import field_validator
from app.core.application.request.base_request import Request
from app.modules.user.domain.exceptions.invalid_dni import InvalidDNIException
from app.modules.user.domain.value_objects.dni import DNI


class CreateTankParams(Request):
    type_id: UUID
    client_dni: str

    @field_validator("client_dni", mode="before")
    @classmethod
    def validate_dni(cls, v):
        if v:
            try:
                return DNI(v)
            except InvalidDNIException as e:
                raise e

        return v
