from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, exists, select, insert
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customer import CustomerAddressTable
from src.schemas.customer_address import (
    CustomerAddressCreateSchema,
    CustomerAddressUpdateSchema,
    CustomerAddressSchema
)
from src.core.exceptions import ObjectDoesNotExistException
from src.utils.validators import (
    validate_customer_address_exist,
    validate_customer_exist,
    validate_unique
)
from src.repositories.customer_address.abstract import CustomerAddressAbcRepo


class CustomerAddressSQLAlchemyRepo(CustomerAddressAbcRepo):
    '''SQLAlchemy CustomerAddress repository.'''

    async def get_by_id(self, id: int, session: AsyncSession) -> CustomerAddressSchema:
        stmt = select(CustomerAddressTable).filter(CustomerAddressTable.id == id)
        res = await session.execute(stmt)
        customer_address_db = res.first()
        if not customer_address_db:
            raise ObjectDoesNotExistException(obj_name='customer_address', obj_id=id)
        
        customer_address_schema = CustomerAddressSchema.model_validate(
            customer_address_db[0]
        )
        return customer_address_schema

    async def get_all(self, session: AsyncSession) -> list[CustomerAddressSchema]:
        stmt = select(CustomerAddressTable)
        res = await session.execute(stmt)
        customer_addresses_schema = [
            CustomerAddressSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return customer_addresses_schema

    async def get_all_by_customer_id(
        self, customer_id: int, session: AsyncSession
    ) -> list[CustomerAddressSchema]:
        await validate_customer_exist(customer_id, session)

        stmt = (
            select(CustomerAddressTable)
            .where(CustomerAddressTable.customer_id == customer_id)
        )
        res = await session.execute(stmt)
        customer_addresses_schema = [
            CustomerAddressSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return customer_addresses_schema

    async def update(
        self,
        id: int,
        update_data: CustomerAddressUpdateSchema,
        session: AsyncSession
    ) -> CustomerAddressSchema:
        data_dict: dict = jsonable_encoder(update_data, exclude_unset=True)

        # TODO: нужно сделать проверку на уникальность address и customer_id!

        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        stmt = (
            update(CustomerAddressTable)
            .where(CustomerAddressTable.id == id)
            .values(data_dict)
            .returning('*')
        )
        res = await session.execute(stmt)
        customer_address_db = res.fetchone()
        if not customer_address_db:
            raise ObjectDoesNotExistException(obj_name='customer_address', obj_id=id)

        await session.commit()

        customer_address_schema = CustomerAddressSchema.model_validate(
            customer_address_db
        )
        return customer_address_schema

    async def create(
        self, create_data: CustomerAddressCreateSchema, session: AsyncSession
    ) -> CustomerAddressSchema:
        data: dict = jsonable_encoder(create_data)

        customer_id: int = data.get('customer_id')
        await validate_customer_exist(customer_id, session)

        await validate_unique(
            CustomerAddressTable, 
            session, 
            expressions_unique = (
                CustomerAddressTable.address == data.get('address'), 
                CustomerAddressTable.customer_id == data.get('customer_id'),
            ),
            unique_together=True
        )

        stmt = insert(CustomerAddressTable).values(**data).returning('*')
        res = await session.execute(stmt)
        customer_address_db = res.fetchone()

        await session.commit()

        customer_address_schema = CustomerAddressSchema.model_validate(
            customer_address_db
        )
        return customer_address_schema

    async def delete(self, id: int, session: AsyncSession) -> None:
        await validate_customer_address_exist(id, session)

        stmt_customer_address = (
            delete(CustomerAddressTable)
            .where(CustomerAddressTable.id == id)
        )

        await session.execute(stmt_customer_address)
        await session.commit()
        return None
