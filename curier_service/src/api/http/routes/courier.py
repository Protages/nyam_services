from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.courier import (
    CourierUpdateSchema,
    CourierCreateSchema,
    CourierSchema
)
from src.database.db import get_async_session
from src.api.http.depends import courier_service
from src.services.courier import CourierService


router = APIRouter(prefix='/courier', tags=['Courier'])


@router.get('/{id}/', response_model=CourierSchema)
async def get_courier_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.get_by_id(id, session)
    return courier_schema


@router.get('/', response_model=list[CourierSchema])
async def get_couriers(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.get_all(session)
    return courier_schema


@router.put('/{id}/', response_model=CourierSchema)
async def update_courier(
    id: int,
    update_courier: CourierUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.update(id, update_courier, session)
    return courier_schema


@router.post('/', response_model=CourierSchema, status_code=status.HTTP_201_CREATED)
async def create_courier(
    courier: CourierCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    courier_schema = await courier_service.create(courier, session)
    return courier_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_courier(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    courier_service: Annotated[CourierService, Depends(courier_service)]
):
    await courier_service.delete(id, session)
    return None
