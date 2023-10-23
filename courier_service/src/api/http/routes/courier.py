from typing import Annotated

from fastapi import APIRouter, status, Depends

from src.schemas.courier import (
    CourierUpdateSchema,
    CourierCreateSchema,
    CourierSchema,
)
from src.schemas.login import TokenPayloadOutputSchema
from src.api.http.depends import courier_service, get_current_user
from src.services.courier import CourierService


router = APIRouter(prefix='/courier', tags=['Courier'])


@router.get('/{id}/', response_model=CourierSchema)
async def get_courier_by_id(
    id: int,
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.get_by_id(id)
    return courier_schema


@router.get('/', response_model=list[CourierSchema])
async def get_couriers(
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.get_all()
    return courier_schema


@router.put('/{id}/', response_model=CourierSchema)
async def update_courier(
    id: int,
    update_courier: CourierUpdateSchema,
    courier_service: Annotated[CourierService, Depends(courier_service)],
    # current_user: Annotated[TokenPayloadOutputSchema, Depends(get_current_user)]
):
    # print('---------', current_user)
    courier_schema = await courier_service.update(id, update_courier)
    return courier_schema


@router.post('/', response_model=CourierSchema, status_code=status.HTTP_201_CREATED)
async def create_courier(
    courier: CourierCreateSchema,
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.create(courier)
    return courier_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_courier(
    id: int,
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    await courier_service.delete(id)
    return None
