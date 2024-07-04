from app.core.domain.exception import DomainException


class InvalidPhoneException(DomainException):
    def __init__(self, phone: str) -> None:
        super().__init__(
            422,
            {
                "type": "invalid_phone",
                "location": ["body", "phone"],
                "msg": f"Invalid phone: {phone}, must be in format '0412-1234567'",
                "input": phone,
            },
        )
