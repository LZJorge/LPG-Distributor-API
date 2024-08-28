from typing import Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.repository import GenericRepository
from app.core.domain.entity import Entity

T = TypeVar("T", bound=Entity)


class GenericSQLRepository(GenericRepository[T]):

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    # Constructing SQL statements
    def _construct_get_stmt(self, id_: str):
        return select(self._model_cls).where(self._model_cls.id == id_)

    def _construct_list_stmt(self, offset: int, limit: int, **filters):
        stmt = select(self._model_cls)
        where_clauses = []

        for column, value in filters.items():
            if not hasattr(self._model_cls, column):
                raise ValueError(f"Invalid column name {column}")

            where_clauses.append(getattr(self._model_cls, column) == value)

        if len(where_clauses) > 0:
            stmt = stmt.where(*where_clauses)

        stmt = stmt.limit(limit).offset(offset)

        return stmt

    # CRUD
    async def add(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        return record

    async def get(self, id_: str) -> T:
        stmt = self._construct_get_stmt(id_)
        r = await self._session.execute(stmt)
        return r.scalars().first()

    async def list(self, offset: int, limit: int, **filters) -> list[T]:
        stmt = self._construct_list_stmt(offset, limit, **filters)
        r = await self._session.execute(stmt)
        return r.scalars().all()

    async def update(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        return record
