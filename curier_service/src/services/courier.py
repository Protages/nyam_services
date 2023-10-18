import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.courier.abstract import CourierAbcRepo
from src.schemas.courier import (
    CourierUpdateSchema, 
    CourierCreateSchema, 
    CourierSchema,
    LoginSchema,
    TokenSchema,
    CourierForGetTokenSchema,
)
from src.core.config import settings
from src.core.exceptions import AnotherServiceException, PasswordInvalidException


class CourierService:
    def __init__(self, courier_repo: type[CourierAbcRepo]) -> None:
        self.courier_repo: CourierAbcRepo = courier_repo()

    def __get_hashed_password(self, password: str) -> str:
        '''Make request on `AUTH_SERIVICE` and return generated hashed password.'''

        url = f'{settings.AUTH_SERIVICE_URL}api/v1/password/get_hashed_password/'
        data = {'row_password': password}
        response: httpx.Response = httpx.post(url, json=data)
        if response.status_code >= 400:
            raise AnotherServiceException(response)
        return response.json().get('hashed_password')

    def __verify_password_and_get_token(
        self, user_id: int, row_password: str, hashed_password: str
    ) -> TokenSchema:
        '''
        Make request on `AUTH_SERIVICE` for verify passed row_password with 
        hashed_password and generate `token` if row_password verify.
        '''

        url = f'{settings.AUTH_SERIVICE_URL}api/v1/token/verify_password_and_get_token/'
        data = {
            'user_id': user_id, 
            'user_type': 'courier',
            'row_password': row_password,
            'hashed_password': hashed_password
        }
        response: httpx.Response = httpx.post(url, json=data)
        if response.status_code >= 400:
            raise AnotherServiceException(response)

        response_data: dict = response.json()
        is_verify: bool = response_data.get('is_verify')
        if not is_verify:
            raise PasswordInvalidException

        token_schema = TokenSchema(
            token=response_data.get('token'),
            token_type=response_data.get('token_type')
        )
        return token_schema

    async def get_by_id(self, id: int, session: AsyncSession) -> CourierSchema:
        res = await self.courier_repo.get_by_id(id, session)
        return res

    async def get_all(self, session: AsyncSession) -> list[CourierSchema]:
        res = await self.courier_repo.get_all(session)
        return res

    async def update(
        self, id: int, update_data: CourierUpdateSchema, session: AsyncSession
    ) -> CourierSchema:
        res = await self.courier_repo.update(id, update_data, session)
        return res

    async def create(
        self, create_data: CourierCreateSchema, session: AsyncSession
    ) -> CourierSchema:
        # replace row password to hashed password
        create_data.password = self.__get_hashed_password(create_data.password)
        res = await self.courier_repo.create(create_data, session)
        return res

    async def delete(self, id: int, session: AsyncSession) -> None:
        res = await self.courier_repo.delete(id, session)
        return res

    async def login(
        self, login_data: LoginSchema, session: AsyncSession
    ) -> TokenSchema:
        courier_schema: CourierForGetTokenSchema = (
            await self.courier_repo.get_by_phone_number(
                phone_number=login_data.phone_number,
                session=session
            )
        )
        token_schema: TokenSchema = self.__verify_password_and_get_token(
            user_id=courier_schema.id,
            row_password=login_data.password,
            hashed_password=courier_schema.password
        )
        return token_schema
