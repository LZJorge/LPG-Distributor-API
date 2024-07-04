import re
from app.modules.user.domain.exceptions.invalid_dni import InvalidDNIException
from app.modules.user.domain.values import DNI_RegEx


class DNI(str):
    """
    Create a new instance of the DNI class.

    Args:
        cls (type): The class object.
        value (str): The DNI value to be validated.

    Raises:
        InvalidDNIException: If the DNI value is invalid.

    Returns:
        str: The newly created DNI object.
    """

    def __new__(cls, value: str) -> str:
        match = re.match(DNI_RegEx, value)

        if not match:
            raise InvalidDNIException(value)

        return super().__new__(cls, value)
