from typing import Optional
from app.core.application.request.base_request import Request


class ListUsersParams(Request):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
