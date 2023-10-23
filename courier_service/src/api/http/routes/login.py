from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.login import LoginSchema, TokenSchema
from src.api.http.depends import courier_service
from src.services.courier import CourierService


router = APIRouter(prefix='/login', tags=['Login'])


@router.post(path='/', response_model=TokenSchema)
async def login(
    data: LoginSchema,
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    token_schema = await courier_service.login(data)
    return token_schema
