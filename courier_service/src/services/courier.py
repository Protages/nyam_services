from src.schemas.courier import (
    CourierUpdateSchema, 
    CourierCreateSchema, 
    CourierSchema,
)
from src.schemas.login import LoginSchema, TokenSchema, CourierForGetTokenSchema
from src.utils.auth import get_hashed_password, verify_password_and_get_token
from src.utils.uow.abstract import UOWBaseAbc


class CourierService:
    def __init__(self, uow: type[UOWBaseAbc]) -> None:
        self.uow: UOWBaseAbc = uow()

    async def get_by_id(self, id: int) -> CourierSchema:
        async with self.uow:
            res = await self.uow.courier_repo.get_by_id(id)
        return res

    async def get_all(self) -> list[CourierSchema]:
        async with self.uow:
            res = await self.uow.courier_repo.get_all()
        return res

    async def update(self, id: int, update_data: CourierUpdateSchema) -> CourierSchema:
        async with self.uow:
            res = await self.uow.courier_repo.update(id, update_data)
            await self.uow.commit()
        return res

    async def create(self, create_data: CourierCreateSchema) -> CourierSchema:
        # replace row password to hashed password
        create_data.password = get_hashed_password(create_data.password)
        async with self.uow:
            res = await self.uow.courier_repo.create(create_data)
            await self.uow.commit()
        return res

    async def delete(self, id: int) -> None:
        async with self.uow:
            res = await self.uow.courier_repo.delete(id)
            await self.uow.commit()
        return res

    async def login(self, login_data: LoginSchema) -> TokenSchema:
        async with self.uow:
            courier_schema: CourierForGetTokenSchema = (
                await self.uow.courier_repo.get_by_phone_number(login_data.phone_number)
            )

        token_schema: TokenSchema = verify_password_and_get_token(
            user_id=courier_schema.id,
            row_password=login_data.password,
            hashed_password=courier_schema.password
        )
        return token_schema
