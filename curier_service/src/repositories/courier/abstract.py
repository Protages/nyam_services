from abc import abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.repository import BaseAbcRepo
from src.schemas.courier import (
    CourierUpdateSchema,
    CourierCreateSchema,
    CourierSchema,
)
from src.schemas.login import CourierForGetTokenSchema


class CourierAbcRepo(BaseAbcRepo):
    '''Base repository for another Courier respositories.'''

    @abstractmethod
    def __init__(self, session: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> CourierSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> CourierForGetTokenSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[CourierSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, update_data: CourierUpdateSchema) -> CourierSchema:
        raise NotImplementedError

    @abstractmethod
    async def create(self, create_data: CourierCreateSchema) -> CourierSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError
