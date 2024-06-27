from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infrastructure.sql_repository import GenericSQLRepository
from app.modules.user.domain.repository import BaseUserRepository
from app.modules.user.domain.entity import User
from app.modules.user.infrastructure.model import UserModel


class UserRepository(GenericSQLRepository[User], BaseUserRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_dni(self, dni: str) -> User:
        stmt = select(self._model_cls).where(self._model_cls.dni == dni)
        r = await self._session.execute(stmt)
        return r.scalars().first()
