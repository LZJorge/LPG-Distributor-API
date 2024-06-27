from app.core.domain.exception import DomainException


class InvalidDNIException(DomainException):
    def __init__(self, dni: str):
        super().__init__(
            400, f"Invalid DNI: {dni}, must be in format 'V-12345678' or 'E-12345678'."
        )
