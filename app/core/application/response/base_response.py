from typing import Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Response(BaseModel, Generic[T]):
    success: bool
    status_code: int
    content: T
    message: Optional[str]
