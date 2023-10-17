from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.restaurant_address import (
    RestaurantAddressSchema,
    RestaurantAddressCreateSchema,
    RestaurantAddressUpdateSchema
)
from src.database.db import get_async_session
from src.api.http.depends import restaurant_address_service
from src.services.restaurant_address import RestaurantAddressService


router = APIRouter(prefix='/restaurant_address', tags=['Restaurant Address'])


@router.get('/{id}/', response_model=RestaurantAddressSchema)
async def get_restaurant_address_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_address_service: Annotated[
        RestaurantAddressService, Depends(restaurant_address_service)
    ]
):
    restaurant_address_schema = await restaurant_address_service.get_by_id(id, session)
    return restaurant_address_schema


@router.get('/', response_model=list[RestaurantAddressSchema])
async def get_restaurants_address(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_address_service: Annotated[
        RestaurantAddressService, Depends(restaurant_address_service)
    ]
):
    restaurant_address_schema = await restaurant_address_service.get_all(session)
    return restaurant_address_schema


@router.get('/restaurant/{restaurant_id}/', response_model=list[RestaurantAddressSchema])
async def get_restaurants_address_by_restaurant_id(
    restaurant_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_address_service: Annotated[
        RestaurantAddressService, Depends(restaurant_address_service)
    ]
):
    restaurant_address_schema = (
        await restaurant_address_service.get_all_by_restaurant_id(
            restaurant_id, session
        )
    )
    return restaurant_address_schema


@router.put('/{id}/', response_model=RestaurantAddressSchema)
async def update_restaurant_address(
    id: int,
    update_restaurant_address: RestaurantAddressUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_address_service: Annotated[
        RestaurantAddressService, Depends(restaurant_address_service)
    ]
):
    restaurant_address_schema = await restaurant_address_service.update(
        id, update_restaurant_address, session
    )
    return restaurant_address_schema


@router.post(
    '/',
    response_model=RestaurantAddressSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_restaurant_address(
    restaurant_address: RestaurantAddressCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_address_service: Annotated[
        RestaurantAddressService, Depends(restaurant_address_service)
    ]
):
    restaurant_address_schema = await restaurant_address_service.create(
        restaurant_address, session
    )
    return restaurant_address_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    restaurant_address_service: Annotated[
        RestaurantAddressService, Depends(restaurant_address_service)
    ]
):
    await restaurant_address_service.delete(id, session)
    return None
