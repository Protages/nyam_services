from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.customer_address import (
    CustomerAddressCreateSchema,
    CustomerAddressUpdateSchema,
    CustomerAddressSchema
)
from src.utils.repository import BaseAbcRepo


class CustomerAddressAbcRepo(BaseAbcRepo):
    '''Base repository for another CustomerAddress respositories.'''

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> CustomerAddressSchema:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[CustomerAddressSchema]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all_by_customer_id(
        self, customer_id: int, session: AsyncSession
    ) -> list[CustomerAddressSchema]:
        raise NotImplementedError()

    @abstractmethod
    async def update(
        self, id: int, update_data: CustomerAddressUpdateSchema, session: AsyncSession
    ) -> CustomerAddressSchema:
        raise NotImplementedError()
    
    @abstractmethod
    async def create(
        self, create_data: CustomerAddressCreateSchema, session: AsyncSession
    ) -> CustomerAddressSchema:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError()
