from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.dish.abstract import DishAbcRepo
from src.schemas.dish import (
    DishCreateSchema,
    DishUpdateSchema,
    DishSchema
)


class DishService:
    def __init__(self, dish_repo: type[DishAbcRepo]) -> None:
        self.dish_repo: DishAbcRepo = dish_repo()

    async def get_by_id(self, id: int, session: AsyncSession) -> DishSchema:
        res = await self.dish_repo.get_by_id(id, session)
        return res
    
    async def get_all(self, session: AsyncSession) -> list[DishSchema]:
        res = await self.dish_repo.get_all(session)
        return res

    async def update(
        self, id: int, update_data: DishUpdateSchema, session: AsyncSession
    ) -> DishSchema:
        res = await self.dish_repo.update(id, update_data, session)
        return res
    
    async def create(
        self, create_data: DishCreateSchema, session: AsyncSession
    ) -> DishSchema:
        res = await self.dish_repo.create(create_data, session)
        return res
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.dish_repo.delete(id, session)
        return res
