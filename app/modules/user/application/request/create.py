from pydantic import field_validator, EmailStr, Field
from app.core.application.request.base_request import Request
from app.modules.user.domain.value_objects.dni import DNI
from app.modules.user.domain.value_objects.phone import Phone

# Exceptions
from app.modules.user.domain.exceptions.invalid_dni import InvalidDNIException
from app.modules.user.domain.exceptions.invalid_phone import InvalidPhoneException


class CreateUserRequest(Request):
    dni: str
    first_name: str = Field(..., min_length=3, max_length=64)
    last_name: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    phone: str
    address: str = Field(..., min_length=3, max_length=255)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, v):
        try:
            return Phone(v)
        except InvalidPhoneException as e:
            raise e

    @field_validator("dni", mode="before")
    @classmethod
    def validate_dni(cls, v):
        try:
            return DNI(v)
        except InvalidDNIException as e:
            raise e
