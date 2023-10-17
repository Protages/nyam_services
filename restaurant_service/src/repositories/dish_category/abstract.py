from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dish_category import (
    DishCategoryCreateSchema,
    DishCategoryUpdateSchema,
    DishCategorySchema
)
from src.schemas.dish import DishSchema
from src.utils.repository import BaseAbcRepo


class DishCategoryAbcRepo(BaseAbcRepo):
    '''Base repository for another DishCategory respositories.'''

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> DishCategorySchema:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[DishCategorySchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_dishes_by_dish_category(
        self, dish_category_id: int, session: AsyncSession
    ) -> list[DishSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, id: int, update_data: DishCategoryUpdateSchema, session: AsyncSession
    ) -> DishCategorySchema:
        raise NotImplementedError
    
    @abstractmethod
    async def create(
        self, create_data: DishCategoryCreateSchema, session: AsyncSession
    ) -> DishCategorySchema:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError
