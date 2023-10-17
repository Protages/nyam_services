from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.customer_address import (
    CustomerAddressCreateSchema,
    CustomerAddressUpdateSchema,
    CustomerAddressSchema
)
from src.repositories.customer_address.abstract import CustomerAddressAbcRepo


class CustomerAddressService:
    def __init__(self, customer_address_repo: type[CustomerAddressAbcRepo]) -> None:
        self.customer_address_repo: CustomerAddressAbcRepo = (
            customer_address_repo()
        )

    async def get_by_id(self, id: int, session: AsyncSession) -> CustomerAddressSchema:
        res = await self.customer_address_repo.get_by_id(id, session)
        return res

    async def get_all(self, session: AsyncSession) -> list[CustomerAddressSchema]:
        res = await self.customer_address_repo.get_all(session)
        return res

    async def get_all_by_customer_id(
        self, customer_id: int, session: AsyncSession
    ) -> list[CustomerAddressSchema]:
        res = await self.customer_address_repo.get_all_by_customer_id(
            customer_id, session
        )
        return res

    async def update(
        self,
        id: int,
        update_data: CustomerAddressUpdateSchema,
        session: AsyncSession
    ) -> CustomerAddressSchema:
        res = await self.customer_address_repo.update(id, update_data, session)
        return res

    async def create(
        self, create_data: CustomerAddressCreateSchema, session: AsyncSession
    ) -> CustomerAddressSchema:
        res = await self.customer_address_repo.create(create_data, session)
        return res

    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.customer_address_repo.delete(id, session)
        return res
