from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.dish_category.abstract import DishCategoryAbcRepo
from src.schemas.dish_category import (
    DishCategoryCreateSchema,
    DishCategoryUpdateSchema,
    DishCategorySchema
)
from src.schemas.dish import DishSchema


class DishCategoryService:
    def __init__(self, dish_category_repo: type[DishCategoryAbcRepo]) -> None:
        self.dish_category_repo: DishCategoryAbcRepo = dish_category_repo()

    async def get_by_id(self, id: int, session: AsyncSession) -> DishCategorySchema:
        res = await self.dish_category_repo.get_by_id(id, session)
        return res
    
    async def get_all(self, session: AsyncSession) -> list[DishCategorySchema]:
        res = await self.dish_category_repo.get_all(session)
        return res
    
    async def get_dishes_by_dish_category(
        self, dish_category_id: int, session: AsyncSession
    ) -> list[DishSchema]:
        res = await self.dish_category_repo.get_dishes_by_dish_category(
            dish_category_id, session
        )
        return res

    async def update(
        self, id: int, update_data: DishCategoryUpdateSchema, session: AsyncSession
    ) -> DishCategorySchema:
        res = await self.dish_category_repo.update(id, update_data, session)
        return res
    
    async def create(
        self, create_data: DishCategoryCreateSchema, session: AsyncSession
    ) -> DishCategorySchema:
        res = await self.dish_category_repo.create(create_data, session)
        return res
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.dish_category_repo.delete(id, session)
        return res
