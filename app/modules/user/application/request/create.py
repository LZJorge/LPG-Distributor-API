from pydantic import field_validator
from app.core.application.request.base_request import Request
from app.modules.user.domain.value_objects.dni import DNI
from app.modules.user.domain.value_objects.phone import Phone


class CreateUserRequest(Request):
    dni: str
    firstname: str
    lastname: str
    email: str
    phone: str
    address: str

    @classmethod
    @field_validator("phone")
    def validate_phone(cls, v):
        return Phone(v)

    @classmethod
    @field_validator("dni")
    def validate_dni(cls, v):
        return DNI(v)
