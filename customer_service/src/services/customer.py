from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.customer import CustomerCreateSchema, CustomerUpdateSchema, CustomerSchema
from src.repositories.customer.abstract import CustomerAbcRepo


class CustomerService:
    def __init__(self, customer_repo: type[CustomerAbcRepo]) -> None:
        self.customer_repo: CustomerAbcRepo = customer_repo()

    async def get_by_id(self, id: int, session: AsyncSession) -> CustomerSchema:
        res = await self.customer_repo.get_by_id(id, session)
        return res

    async def get_all(self, session: AsyncSession) -> list[CustomerSchema]:
        res = await self.customer_repo.get_all(session)
        return res

    async def update(
        self, id: int, update_data: CustomerUpdateSchema, session: AsyncSession
    ) -> CustomerSchema:
        res = await self.customer_repo.update(id, update_data, session)
        return res

    async def create(
        self, create_data: CustomerCreateSchema, session: AsyncSession
    ) -> CustomerSchema:
        res = await self.customer_repo.create(create_data, session)
        return res

    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.customer_repo.delete(id, session)
        return res
