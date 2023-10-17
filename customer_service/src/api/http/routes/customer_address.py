from typing import Annotated

from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.schemas.customer_address import (
    CustomerAddressSchema,
    CustomerAddressCreateSchema,
    CustomerAddressUpdateSchema,
)
from src.services.customer_address import CustomerAddressService
from src.api.http.depends import customer_address_service


router = APIRouter(prefix='/customer_address', tags=['Customer Address'])


@router.get('/{id}/', response_model=CustomerAddressSchema)
async def get_customer_address_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_address_service: Annotated[
        CustomerAddressService, Depends(customer_address_service)
    ]
):
    customer_address_schema = await customer_address_service.get_by_id(id, session)
    return customer_address_schema


@router.get('/', response_model=list[CustomerAddressSchema])
async def get_all_customer_address(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_address_service: Annotated[
        CustomerAddressService, Depends(customer_address_service)
    ]
):
    customer_address_schema = await customer_address_service.get_all(session)
    return customer_address_schema


@router.get('/customer/{customer_id}/', response_model=list[CustomerAddressSchema])
async def get_all_customer_address_by_customer_id(
    customer_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_address_service: Annotated[
        CustomerAddressService, Depends(customer_address_service)
    ]
):
    customer_address_schema = await customer_address_service.get_all_by_customer_id(
        customer_id, session
    )
    return customer_address_schema


@router.put('/{id}/', response_model=CustomerAddressSchema)
async def update_customer_address(
    id: int,
    customer_address_update: CustomerAddressUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_address_service: Annotated[
        CustomerAddressService, Depends(customer_address_service)
    ]
):
    customer_address_schema = await customer_address_service.update(
        id, customer_address_update, session
    )
    return customer_address_schema


@router.post(
    '/',
    response_model=CustomerAddressSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_customer_address(
    customer_address: CustomerAddressCreateSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_address_service: Annotated[
        CustomerAddressService, Depends(customer_address_service)
    ]
):
    customer_address_schema = await customer_address_service.create(
        customer_address, session
    )
    return customer_address_schema


@router.delete('/{id}/', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_address(
    id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    customer_address_service: Annotated[
        CustomerAddressService, Depends(customer_address_service)
    ]
):
    await customer_address_service.delete(id, session)
    return None
