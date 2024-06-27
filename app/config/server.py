import sys
import asyncio
import uvicorn

from fastapi import FastAPI
from app.utils.add_routers import add_routers
from app.modules.user.infrastructure.router import UserRouter

routers = [UserRouter()]


class App:
    _server: FastAPI = None

    def __init__(self) -> None:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        self._server = FastAPI()

        add_routers(self._server, routers)

    def start(self) -> None:
        uvicorn.run(self._server, host="127.0.0.1", port=8000)
