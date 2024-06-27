from app.core.domain.exception import DomainException


class InvalidPhoneException(DomainException):
    def __init__(self, phone: str) -> None:
        super().__init__(
            400,
            {
                "message": "Phone must be in format '0412-1234567'.",
                "phone": phone,
            },
        )
