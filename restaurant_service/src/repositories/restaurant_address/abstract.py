from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.restaurant_address import (
    RestaurantAddressCreateSchema,
    RestaurantAddressUpdateSchema,
    RestaurantAddressSchema
)
from src.utils.repository import BaseAbcRepo


class RestaurantAddressAbcRepo(BaseAbcRepo):
    '''Base repository for another RestaurantAddress respositories.'''

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> RestaurantAddressSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[RestaurantAddressSchema]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_by_restaurant_id(
        self, restaurant_id: int, session: AsyncSession
    ) -> list[RestaurantAddressSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, id: int, update_data: RestaurantAddressUpdateSchema, session: AsyncSession
    ) -> RestaurantAddressSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def create(
        self, create_data: RestaurantAddressCreateSchema, session: AsyncSession
    ) -> RestaurantAddressSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError
