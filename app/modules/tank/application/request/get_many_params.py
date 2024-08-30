from typing import Optional

from pydantic import field_validator
from app.core.application.request.base_request import Request
from app.modules.user.domain.exceptions.invalid_dni import InvalidDNIException
from app.modules.user.domain.value_objects.dni import DNI


class GetManyTanksParams(Request):
    type: Optional[str] = None
    delivered: Optional[bool] = None
    created_at: Optional[str] = None
    client_dni: Optional[str] = None

    @field_validator("client_dni", mode="after")
    @classmethod
    def validate_dni(cls, v):
        if v:
            try:
                return DNI(v)
            except InvalidDNIException as e:
                raise e

        return v
