from fastapi import FastAPI
from app.core.infrastructure.router import BaseRouter


def add_routers(app: FastAPI, routers: list[BaseRouter]) -> None:
    for instance in routers:
        router = instance.get_router()

        app.include_router(router)
