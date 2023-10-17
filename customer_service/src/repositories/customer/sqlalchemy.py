from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, exists, select, insert
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customer import CustomerTable, CustomerAddressTable
from src.schemas.customer import CustomerCreateSchema, CustomerUpdateSchema, CustomerSchema
from src.core.exceptions import ObjectDoesNotExistException
from src.utils.validators import validate_customer_exist, validate_unique
from src.repositories.customer.abstract import CustomerAbcRepo


class CustomerSQLAlchemyRepo(CustomerAbcRepo):
    '''SQLAlchemy Customer repository.'''

    async def get_by_id(self, id: int, session: AsyncSession) -> CustomerSchema:
        stmt = select(CustomerTable).filter(CustomerTable.id == id)
        res = await session.execute(stmt)
        customer_db = res.fetchone()
        if not customer_db:
            raise ObjectDoesNotExistException(obj_name='customer', obj_id=id)

        customer_schema = CustomerSchema.model_validate(customer_db[0])
        return customer_schema

    async def get_all(self, session: AsyncSession) -> list[CustomerSchema]:
        stmt = select(CustomerTable)
        res = await session.execute(stmt)
        customers_schema = [
            CustomerSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return customers_schema

    async def update(
        self, id: int, update_data: CustomerUpdateSchema, session: AsyncSession
    ) -> CustomerSchema:
        data_dict: dict = jsonable_encoder(update_data, exclude_unset=True)

        await validate_unique(
            CustomerTable,
            session=session,
            expressions_unique=(
                CustomerTable.email == data_dict.get('email'),
            ),
        )

        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        stmt = (
            update(CustomerTable)
            .where(CustomerTable.id == id)
            .values(data_dict)
            .returning('*')
        )
        res = await session.execute(stmt)
        customer_db = res.fetchone()
        if not customer_db:
            raise ObjectDoesNotExistException(obj_name='customer', obj_id=id)

        await session.commit()

        customer_schema = CustomerSchema.model_validate(customer_db)
        return customer_schema

    async def create(
        self, create_data: CustomerCreateSchema, session: AsyncSession
    ) -> CustomerSchema:
        data_dict: dict = jsonable_encoder(create_data, exclude={'password'})

        await validate_unique(
            CustomerTable,
            session=session,
            expressions_unique=(
                CustomerTable.email == data_dict.get('email'),
                CustomerTable.phone_number == data_dict.get('phone_number')
            ),
            unique_together=False
        )
        
        hashed_password = create_data.password + 'HS256'
        data_dict['password'] = hashed_password

        stmt = insert(CustomerTable).values(**data_dict).returning('*')
        res = await session.execute(stmt)
        customer_db = res.fetchone()

        await session.commit()

        customer_schema = CustomerSchema.model_validate(customer_db)
        return customer_schema

    async def delete(self, id: int, session: AsyncSession) -> None:
        await validate_customer_exist(id, session)

        # also delete related CustomerAddress records
        # stmt_customer_address = (
        #     delete(CustomerAddressTable)
        #     .where(CustomerAddressTable.customer_id == id)
        # )
        stmt_customer = delete(CustomerTable).where(CustomerTable.id == id)

        # await session.execute(stmt_customer_address)
        await session.execute(stmt_customer)
        await session.commit()

        return None
