from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.client.domain.entity import Client
from app.modules.client.infrastructure.model import ClientModel
from app.modules.client.domain.repository import BaseClientRepository
from app.core.infrastructure.sql_repository import GenericSQLRepository


class ClientRepository(GenericSQLRepository[Client], BaseClientRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ClientModel)

    async def get_by_dni(self, dni: str) -> Client:
        stmt = select(self._model_cls).where(self._model_cls.user.dni == dni)
        r = await self._session.execute(stmt)
        return r.scalars().first()
    
    async def get_by_user_id(self, user_id: str) -> Client:
        stmt = select(self._model_cls).where(self._model_cls.user_id == user_id)
        r = await self._session.execute(stmt)
        return r.scalars().first()