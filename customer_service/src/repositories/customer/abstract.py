from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.customer import CustomerCreateSchema, CustomerUpdateSchema, CustomerSchema
from src.utils.repository import BaseAbcRepo


class CustomerAbcRepo(BaseAbcRepo):
    '''Base repository for another Customer respositories.'''
    
    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> CustomerSchema:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[CustomerSchema]:
        raise NotImplementedError()
    
    @abstractmethod
    async def update(
        self, id: int, update_data: CustomerUpdateSchema, session: AsyncSession
    ) -> CustomerSchema:
        raise NotImplementedError()
    
    @abstractmethod
    async def create(
        self, create_data: CustomerCreateSchema, session: AsyncSession
    ) -> CustomerSchema:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError()
