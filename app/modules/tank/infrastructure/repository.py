from sqlalchemy.ext.asyncio import AsyncSession
from app.core.infrastructure.sql_repository import GenericSQLRepository
from app.modules.client.infrastructure.model import ClientModel
from app.modules.tank.domain.entity import Tank, TankType
from app.modules.tank.infrastructure.model import TankModel, TankTypeModel
from app.modules.tank.domain.repository import (
    BaseTankRepository,
    BaseTankTypeRepository,
)
from app.modules.user.infrastructure.model import UserModel


class TankRepository(GenericSQLRepository[Tank], BaseTankRepository):

    async def list(self, offset: int, limit: int, **filters) -> list[Tank]:
        filtered_args = {
            key: value
            for key, value in filters.items()
            if key != "client_dni" and key != "type"
        }

        stmt = (
            super()
            ._construct_list_stmt(offset, limit, **filtered_args)
            .join(ClientModel)
        )

        if "type" in filters and filters["type"]:
            stmt = stmt.join(TankTypeModel).filter(
                TankTypeModel.name.ilike(f"%{filters['type']}%")
            )

        if "client_dni" in filters and filters["client_dni"]:
            stmt = stmt.join(UserModel).filter_by(dni=filters["client_dni"])

        r = await self._session.execute(stmt)
        return r.scalars().all()

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TankModel)


class TankTypesRepository(GenericSQLRepository[TankType], BaseTankTypeRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TankTypeModel)
