from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.restaurant.abstract import RestaurantAbcRepo
from src.schemas.restaurant import (
    RestaurantCreateSchema,
    RestaurantUpdateSchema,
    RestaurnatSchema
)


class RestaurantService:
    def __init__(self, restaurant_repo: type[RestaurantAbcRepo]) -> None:
        self.restaurant_repo: RestaurantAbcRepo = restaurant_repo()

    async def get_by_id(self, id: int, session: AsyncSession) -> RestaurnatSchema:
        res = await self.restaurant_repo.get_by_id(id, session)
        return res
    
    async def get_all(self, session: AsyncSession) -> list[RestaurnatSchema]:
        res = await self.restaurant_repo.get_all(session)
        return res

    async def update(
        self, id: int, update_data: RestaurantUpdateSchema, session: AsyncSession
    ) -> RestaurnatSchema:
        res = await self.restaurant_repo.update(id, update_data, session)
        return res
    
    async def create(
        self, create_data: RestaurantCreateSchema, session: AsyncSession
    ) -> RestaurnatSchema:
        res = await self.restaurant_repo.create(create_data, session)
        return res
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.restaurant_repo.delete(id, session)
        return res
