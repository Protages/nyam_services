from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.restaurant import (
    RestaurnatSchema,
    RestaurantCreateSchema,
    RestaurantUpdateSchema
)
from src.database.db import get_async_session
from src.api.http.depends import restaurant_service
from src.services.restaurant import RestaurantService


router = APIRouter(prefix='/restaurant', tags=['Restaurant'])


@router.get('/{id}/', response_model=RestaurnatSchema)
async def get_restaurant_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_service: Annotated[RestaurantService, Depends(restaurant_service)]
):
    restaurant_schema = await restaurant_service.get_by_id(id, session)
    return restaurant_schema


@router.get('/', response_model=list[RestaurnatSchema])
async def get_restaurants(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_service: Annotated[RestaurantService, Depends(restaurant_service)]
):
    restaurant_schema = await restaurant_service.get_all(session)
    return restaurant_schema


@router.put('/{id}/', response_model=RestaurnatSchema)
async def update_restaurant(
    id: int,
    update_restaurant: RestaurantUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_service: Annotated[RestaurantService, Depends(restaurant_service)]
):
    restaurant_schema = await restaurant_service.update(id, update_restaurant, session)
    return restaurant_schema


@router.post('/', response_model=RestaurnatSchema, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    restaurant: RestaurantCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_service: Annotated[RestaurantService, Depends(restaurant_service)]
):
    restaurant_schema = await restaurant_service.create(restaurant, session)
    return restaurant_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_service: Annotated[RestaurantService, Depends(restaurant_service)]
):
    await restaurant_service.delete(id, session)
    return None
