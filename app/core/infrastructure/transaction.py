from app.config.database import session_factory
from app.core.domain.transaction import GenericTransaction


class Transaction(GenericTransaction):

    def __init__(self, **repositories) -> None:
        self._session_factory = session_factory
        self._repositories = repositories

    async def __aenter__(self):
        self._session = self._session_factory()

        for name, repository in self._repositories.items():
            setattr(self, name, repository(self._session))

        return await super().__aenter__()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()


def get_transaction() -> GenericTransaction:
    return Transaction
