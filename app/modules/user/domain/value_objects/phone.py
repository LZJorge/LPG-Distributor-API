import re
from app.modules.user.domain.exceptions.invalid_phone import InvalidPhoneException
from app.modules.user.domain.values import PHONE_RegEx


class Phone(str):
    """
    Validates the phone number by checking if it matches the defined in PHONE_RegEx.

    Args:
        cls (Type[Phone]): The class object.
        value (str): The phone number to be validated.

    Raises:
        InvalidPhoneException: If the phone number is invalid.

    Returns:
        str: The newly created Phone object.
    """

    def __new__(cls, value: str) -> "Phone":
        match = re.match(PHONE_RegEx, value)

        if not match:
            raise InvalidPhoneException(f"Invalid Phone: {value}")

        return super().__new__(cls, value)
