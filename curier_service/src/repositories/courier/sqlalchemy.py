from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.courier import CourierUpdateSchema, CourierCreateSchema, CourierSchema
from src.repositories.courier.abstract import CourierAbcRepo


class CourierSQLAlchemyRepo(CourierAbcRepo):
    async def get_by_id(self, id: int, session: AsyncSession) -> CourierSchema:
        res = await self.courier_repo.get_by_id(id, session)
        return res
    
    async def get_all(self, session: AsyncSession) -> list[CourierSchema]:
        res = await self.courier_repo.get_all(session)
        return res
    
    async def update(
        self, id: int, update_data: CourierUpdateSchema, session: AsyncSession
    ) -> CourierSchema:
        res = await self.courier_repo.update(id, update_data, session)
        return res
    
    async def create(
        self, create_data: CourierCreateSchema, session: AsyncSession
    ) -> CourierSchema:
        res = await self.courier_repo.create(create_data, session)
        return res
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.courier_repo.delete(id, session)
        return res
