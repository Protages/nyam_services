from fastapi import APIRouter

from src.schemas.password import (
    HashedPasswordInputSchema,
    HashedPasswordOutputSchema,
    VerifyPasswordInputSchema,
    VerifyPasswordOutputSchema,
)
from src.core.security import get_password_hash, is_verify_password


router = APIRouter(prefix='/password', tags=['Password'])


@router.post(path='/get_hashed_password/', response_model=HashedPasswordOutputSchema)
async def generate_hashed_password(row_password: HashedPasswordInputSchema):
    hashed_password = get_password_hash(row_password.row_password)
    res_schema = HashedPasswordOutputSchema(hashed_password=hashed_password)
    return res_schema


@router.post(path='/verify_password/', response_model=VerifyPasswordOutputSchema)
async def verify_password(data: VerifyPasswordInputSchema):
    is_verifiy = is_verify_password(data.row_password, data.hashed_password)
    res_schema = VerifyPasswordOutputSchema(is_verify=is_verifiy)
    return res_schema
