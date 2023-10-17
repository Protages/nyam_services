from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, select, insert
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.restaurant_address.abstract import RestaurantAddressAbcRepo
from src.schemas.restaurant_address import (
    RestaurantAddressCreateSchema,
    RestaurantAddressUpdateSchema,
    RestaurantAddressSchema
)
from src.models.restaurant import RestaurantAddressTable
from src.core.exceptions import ObjectDoesNotExistException
from src.utils.validators import (
    validate_unique, 
    validate_restaurant_exist, 
    validate_restaurant_address_exist
)


class RestaurantAddressSQLAlchemyRepo(RestaurantAddressAbcRepo):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> RestaurantAddressSchema:
        stmt = select(RestaurantAddressTable).where(RestaurantAddressTable.id == id)
        res = await session.execute(stmt)
        restaurant_address_db = res.fetchone()
        if not restaurant_address_db:
            raise ObjectDoesNotExistException(obj_name='restaurant_address', obj_id=id)

        restaurant_address_schema = RestaurantAddressSchema.model_validate(
            restaurant_address_db[0]
        )
        return restaurant_address_schema
    
    async def get_all(self, session: AsyncSession) -> list[RestaurantAddressSchema]:
        stmt = select(RestaurantAddressTable)
        res = await session.execute(stmt)
        restaurant_addresses_schema = [
            RestaurantAddressSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return restaurant_addresses_schema
    
    async def get_all_by_restaurant_id(
        self, restaurant_id: int, session: AsyncSession
    ) -> list[RestaurantAddressSchema]:
        await validate_restaurant_exist(restaurant_id, session)

        stmt = (
            select(RestaurantAddressTable)
            .where(RestaurantAddressTable.restaurant_id == restaurant_id)
        )
        res = await session.execute(stmt)
        restaurant_addresses_schema = [
            RestaurantAddressSchema.model_validate(item[0])
            for item in res.fetchall()
        ]

        return restaurant_addresses_schema
    
    async def update(
        self, id: int, update_data: RestaurantAddressUpdateSchema, session: AsyncSession
    ) -> RestaurantAddressSchema:
        data_dict: dict = jsonable_encoder(update_data, exclude_unset=True)
        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        stmt = (
            update(RestaurantAddressTable)
            .where(RestaurantAddressTable.id == id)
            .values(data_dict)
            .returning('*')
        )
        res = await session.execute(stmt)
        restaurant_db = res.fetchone()
        if not restaurant_db:
            raise ObjectDoesNotExistException(obj_name='restaurant_address', obj_id=id)

        await session.commit()

        restaurant_schema = RestaurantAddressSchema.model_validate(restaurant_db)
        return restaurant_schema
    
    async def create(
        self, create_data: RestaurantAddressCreateSchema, session: AsyncSession
    ) -> RestaurantAddressSchema:
        data_dict: dict = jsonable_encoder(create_data, exclude_unset=True)

        await validate_unique(
            table=RestaurantAddressTable,
            session=session,
            expressions_unique=(
                RestaurantAddressTable.address == data_dict.get('address'),
                RestaurantAddressTable.restaurant_id == data_dict.get('restaurant_id')
            ),
            unique_together=True
        )

        stmt = insert(RestaurantAddressTable).values(**data_dict).returning('*')
        res = await session.execute(stmt)
        restaurant_db = res.fetchone()

        await session.commit()

        restaurant_schema = RestaurantAddressSchema.model_validate(restaurant_db)
        return restaurant_schema
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        await validate_restaurant_address_exist(id, session)

        stmt = (
            delete(RestaurantAddressTable)
            .where(RestaurantAddressTable.id == id)
        )

        async with session.begin():
            await session.execute(stmt)
            await session.commit()

        return None
