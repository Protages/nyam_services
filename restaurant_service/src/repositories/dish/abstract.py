from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dish import (
    DishCreateSchema,
    DishUpdateSchema,
    DishSchema
)
from src.utils.repository import BaseAbcRepo


class DishAbcRepo(BaseAbcRepo):
    '''Base repository for another Dish respositories.'''

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> DishSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[DishSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, id: int, update_data: DishUpdateSchema, session: AsyncSession
    ) -> DishSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def create(
        self, create_data: DishCreateSchema, session: AsyncSession
    ) -> DishSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError
