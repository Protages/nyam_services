from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dish_category import (
    DishCategoryCreateSchema,
    DishCategoryUpdateSchema,
    DishCategorySchema
)
from src.schemas.dish import DishSchema
from src.database.db import get_async_session
from src.api.http.depends import dish_category_service
from src.services.dish_category import DishCategoryService


router = APIRouter(prefix='/dish_category', tags=['Dish Category'])


@router.get('/{id}/', response_model=DishCategorySchema)
async def get_dish_category_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_category_service: Annotated[DishCategoryService, Depends(dish_category_service)]
):
    dish_category_schema = await dish_category_service.get_by_id(id, session)
    return dish_category_schema


@router.get('/', response_model=list[DishCategorySchema])
async def get_dishes_category(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_category_service: Annotated[DishCategoryService, Depends(dish_category_service)]
):
    dishes_category_schema = await dish_category_service.get_all(session)
    return dishes_category_schema


@router.get('/{id}/dishes/', response_model=list[DishSchema])
async def get_dishes_by_dish_category(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_category_service: Annotated[DishCategoryService, Depends(dish_category_service)]
):
    dishes_schema = await dish_category_service.get_dishes_by_dish_category(
        id, session
    )
    return dishes_schema


@router.put('/{id}/', response_model=DishCategorySchema)
async def update_dish_category(
    id: int,
    update_dish_category: DishCategoryUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_category_service: Annotated[DishCategoryService, Depends(dish_category_service)]
):
    dish_category_schema = await dish_category_service.update(
        id, update_dish_category, session
    )
    return dish_category_schema


@router.post('/', response_model=DishCategorySchema, status_code=status.HTTP_201_CREATED)
async def create_dish_category(
    dish_category: DishCategoryCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_category_service: Annotated[DishCategoryService, Depends(dish_category_service)]
):
    dish_category_schema = await dish_category_service.create(dish_category, session)
    return dish_category_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish_category(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    dish_category_service: Annotated[DishCategoryService, Depends(dish_category_service)]
):
    await dish_category_service.delete(id, session)
    return None
