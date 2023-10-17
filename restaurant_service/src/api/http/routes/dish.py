from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dish import (
    DishSchema,
    DishCreateSchema,
    DishUpdateSchema
)
from src.database.db import get_async_session
from src.api.http.depends import dish_service
from src.services.dish import DishService


router = APIRouter(prefix='/dish', tags=['Dish'])


@router.get('/{id}/', response_model=DishSchema)
async def get_dish_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_service: Annotated[DishService, Depends(dish_service)]
):
    dish_schema = await dish_service.get_by_id(id, session)
    return dish_schema


@router.get('/', response_model=list[DishSchema])
async def get_dishs(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_service: Annotated[DishService, Depends(dish_service)]
):
    dish_schema = await dish_service.get_all(session)
    return dish_schema


@router.put('/{id}/', response_model=DishSchema)
async def update_dish(
    id: int,
    update_dish: DishUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_service: Annotated[DishService, Depends(dish_service)]
):
    dish_schema = await dish_service.update(id, update_dish, session)
    return dish_schema


@router.post('/', response_model=DishSchema, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish: DishCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_service: Annotated[DishService, Depends(dish_service)]
):
    dish_schema = await dish_service.create(dish, session)
    return dish_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_service: Annotated[DishService, Depends(dish_service)]
):
    await dish_service.delete(id, session)
    return None
