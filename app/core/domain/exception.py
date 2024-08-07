from typing import Dict
from fastapi.exceptions import HTTPException


class DomainException(HTTPException):
    def __init__(self, status_code: int, detail: Dict[str, str]):
        super().__init__(status_code=status_code, detail={**detail})
