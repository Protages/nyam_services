from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.restaurant import (
    RestaurantCreateSchema,
    RestaurantUpdateSchema,
    RestaurnatSchema
)
from src.utils.repository import BaseAbcRepo


class RestaurantAbcRepo(BaseAbcRepo):
    '''Base repository for another Restaurant respositories.'''

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> RestaurnatSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[RestaurnatSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, id: int, update_data: RestaurantUpdateSchema, session: AsyncSession
    ) -> RestaurnatSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def create(
        self, create_data: RestaurantCreateSchema, session: AsyncSession
    ) -> RestaurnatSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError
