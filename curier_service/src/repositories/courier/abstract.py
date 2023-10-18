from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.repository import BaseAbcRepo
from src.schemas.courier import (
    CourierUpdateSchema,
    CourierCreateSchema,
    CourierSchema,
    LoginSchema,
    TokenSchema,
    CourierForGetTokenSchema,
)


class CourierAbcRepo(BaseAbcRepo):
    '''Base repository for another Courier respositories.'''

    @abstractmethod
    async def get_by_id(self, id: int, session: AsyncSession) -> CourierSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_phone_number(
        self, phone_number: str, session: AsyncSession
    ) -> CourierForGetTokenSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[CourierSchema]:
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        self, id: int, update_data: CourierUpdateSchema, session: AsyncSession
    ) -> CourierSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def create(
        self, create_data: CourierCreateSchema, session: AsyncSession
    ) -> CourierSchema:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id: int, session: AsyncSession) -> None:
        raise NotImplementedError
