from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_async_session
from src.services.customer import CustomerService
from src.services.customer_address import CustomerAddressService
from src.repositories.customer.sqlalchemy import CustomerSQLAlchemyRepo
from src.repositories.customer_address.sqlalchemy import CustomerAddressSQLAlchemyRepo


def customer_service():
    '''Return CustomerService with `CustomerSQLAlchemyRepo`.'''
    return CustomerService(CustomerSQLAlchemyRepo)


def customer_address_service():
    '''Return CustomerAddressService with `CustomerAddressSQLAlchemyRepo`.'''
    return CustomerAddressService(CustomerAddressSQLAlchemyRepo)


# from src.database.db import SessionLocal
# def get_sync_session():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
