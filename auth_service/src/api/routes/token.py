from datetime import timedelta

from fastapi import APIRouter

from src.schemas.token import (
    GetTokenInputSchema,
    GetTokenOutputSchema,
    VerifyPasswordAndGetTokenInputSchema,
    VerifyPasswordAndGetTokenOutputSchema,
    VerifyTokenInputSchema,
    VerifyTokenOutputSchema,
)
from src.core.security import is_verify_password, get_token, verify_token
from src.core.config import settings
from src.core.exceptions import PasswordInvalidException


router = APIRouter(prefix='/token', tags=['Token'])
expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.post(
    path='/get_token/', 
    response_model=GetTokenOutputSchema, 
    description='Генерирует токен на основе переданного `user_id` '
    'юзера и `user_type` и возвращает его.'
)
async def generate_token(data: GetTokenInputSchema):
    data_to_encode = {'user_id': data.user_id, 'user_type': data.user_type}
    token: str = get_token(data_to_encode, expires_delta)
    res_schema = GetTokenOutputSchema(token=token, token_type=settings.TOKEN_TYPE)
    return res_schema


@router.post(
    path='/verify_password_and_get_token/',
    response_model=VerifyPasswordAndGetTokenOutputSchema,
    description='Одновременно генерирует токен и верифицирует равен ли сырой пароль '
    '(`row_password`) захешированному пароль (`hashed_password`).\n\n'
    'Если равен, то генерирует '
    'токен на основе переданного `user_id` юзера и `user_type` и возвращает его.\n\n'
    'Если не равен, возвращает статус 401 и сообщение ошибки.'
)
async def verify_password_and_generate_token(
    data: VerifyPasswordAndGetTokenInputSchema
):
    is_verify: bool = is_verify_password(
        row_password=data.row_password,
        hashed_password=data.hashed_password
    )
    if not is_verify:
        raise PasswordInvalidException
    else:
        data_to_encode = {'user_id': data.user_id, 'user_type': data.user_type}
        token: str = get_token(data_to_encode, expires_delta)
        res_schema = VerifyPasswordAndGetTokenOutputSchema(
            is_verify=is_verify, token=token, token_type=settings.TOKEN_TYPE
        )
        return res_schema


@router.post(
    path='/verify_token/', 
    response_model=VerifyTokenOutputSchema,
    description='Верифицирует токен, если токен не валиден возвращает соответсвующую '
    'ошибку. Если валадиен, вернет его `payload`.'
)
async def verify_token_valid(token: VerifyTokenInputSchema):
    token_schema: VerifyTokenOutputSchema = verify_token(token=token.token)
    return token_schema
