from abc import ABC, abstractmethod
from fastapi import APIRouter


class BaseRouter(ABC):
    __prefix__: str
    __tag__: str

    def __init__(self, instance: APIRouter) -> None:
        self._router = instance

        self._register_routes()

    @abstractmethod
    def _register_routes(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_router(self) -> APIRouter:
        raise NotImplementedError
