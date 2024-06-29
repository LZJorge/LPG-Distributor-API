from typing import AsyncGenerator

from anyio import get_current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import settings

engine = create_async_engine(settings.database_url)

session_factory = async_scoped_session(
    sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    ),
    scopefunc=get_current_task,
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_factory()

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        await session.close()
