import asyncio
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.modules.client.infrastructure.router import ClientRouter
from app.modules.user.infrastructure.router import UserRouter

# Utils
from app.utils.add_routers import add_routers

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# API
app = FastAPI()
routers = [UserRouter(), ClientRouter()]

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routers(app, routers)
