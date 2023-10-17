from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.restaurant_address.abstract import RestaurantAddressAbcRepo
from src.schemas.restaurant_address import (
    RestaurantAddressSchema,
    RestaurantAddressCreateSchema,
    RestaurantAddressUpdateSchema
)


class RestaurantAddressService:
    def __init__(self, restaurant_address_repo: type[RestaurantAddressAbcRepo]) -> None:
        self.restaurant_address_repo: RestaurantAddressAbcRepo = restaurant_address_repo()

    async def get_by_id(self, id: int, session: AsyncSession) -> RestaurantAddressSchema:
        res = await self.restaurant_address_repo.get_by_id(id, session)
        return res
    
    async def get_all(self, session: AsyncSession) -> list[RestaurantAddressSchema]:
        res = await self.restaurant_address_repo.get_all(session)
        return res
    
    async def get_all_by_restaurant_id(
        self, restaurant_id: int, session: AsyncSession
    ) -> list[RestaurantAddressSchema]:
        res = await self.restaurant_address_repo.get_all_by_restaurant_id(
            restaurant_id, session
        )
        return res

    async def update(
        self, id: int, update_data: RestaurantAddressUpdateSchema, session: AsyncSession
    ) -> RestaurantAddressSchema:
        res = await self.restaurant_address_repo.update(id, update_data, session)
        return res
    
    async def create(
        self, create_data: RestaurantAddressCreateSchema, session: AsyncSession
    ) -> RestaurantAddressSchema:
        res = await self.restaurant_address_repo.create(create_data, session)
        return res
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.restaurant_address_repo.delete(id, session)
        return res
