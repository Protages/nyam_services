from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.customer import (
    CustomerSchema,
    CustomerCreateSchema,
    CustomerUpdateSchema
)
from src.database.db import get_async_session
from src.api.http.depends import customer_service
from src.services.customer import CustomerService


router = APIRouter(prefix='/customer', tags=['Customer'])


@router.get('/{id}/', response_model=CustomerSchema)
async def get_customer_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_service: Annotated[CustomerService, Depends(customer_service)]
):
    customer_schema = await customer_service.get_by_id(id, session)
    return customer_schema


@router.get('/', response_model=list[CustomerSchema])
async def get_customers(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_service: Annotated[CustomerService, Depends(customer_service)]
):
    customer_schema = await customer_service.get_all(session)
    return customer_schema


@router.put('/{id}/', response_model=CustomerSchema)
async def update_customer(
    id: int,
    update_customer: CustomerUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_service: Annotated[CustomerService, Depends(customer_service)]
):
    customer_schema = await customer_service.update(id, update_customer, session)
    return customer_schema


@router.post('/', response_model=CustomerSchema, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer: CustomerCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_service: Annotated[CustomerService, Depends(customer_service)]
):
    customer_schema = await customer_service.create(customer, session)
    return customer_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_service: Annotated[CustomerService, Depends(customer_service)]
):
    await customer_service.delete(id, session)
    return None
