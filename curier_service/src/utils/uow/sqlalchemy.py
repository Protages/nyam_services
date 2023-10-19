from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_sqlite_session_maker
from src.utils.uow.abstract import UOWBaseAbc
from src.repositories.courier.sqlalchemy import CourierSQLAlchemyRepo


class UOWSQLAlchemy(UOWBaseAbc):
    def __init__(self) -> None:
        self.session_factory = async_sqlite_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.courier_repo = CourierSQLAlchemyRepo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
        await self.session.close()
