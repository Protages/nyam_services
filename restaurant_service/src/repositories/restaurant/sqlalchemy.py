from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, select, insert
from sqlalchemy.orm import Session
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.restaurant.abstract import RestaurantAbcRepo
from src.schemas.restaurant import RestaurantCreateSchema, RestaurantUpdateSchema, RestaurnatSchema
from src.models.restaurant import RestaurantTable, RestaurantAddressTable
from src.models.dish import DishTable
from src.core.exceptions import ObjectDoesNotExistException
from src.utils.validators import validate_unique, validate_restaurant_exist


class RestaurantSQLAlchemyRepo(RestaurantAbcRepo):
    async def get_by_id(self, id: int, session: AsyncSession) -> RestaurnatSchema:
        stmt = select(RestaurantTable).where(RestaurantTable.id == id)
        res = await session.execute(stmt)
        restaurant_db = res.fetchone()
        if not restaurant_db:
            raise ObjectDoesNotExistException(obj_name='restaurant', obj_id=id)

        restaurant_schema = RestaurnatSchema.model_validate(restaurant_db[0])
        return restaurant_schema
    
    async def get_all(self, session: AsyncSession) -> list[RestaurnatSchema]:
        stmt = select(RestaurantTable)
        res = await session.execute(stmt)
        restaurants_schema = [
            RestaurnatSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return restaurants_schema
    
    async def update(
        self, id: int, update_data: RestaurantUpdateSchema, session: AsyncSession
    ) -> RestaurnatSchema:
        data_dict: dict = jsonable_encoder(update_data, exclude_unset=True)
        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        stmt = (
            update(RestaurantTable)
            .where(RestaurantTable.id == id)
            .values(data_dict)
            .returning('*')
        )
        res = await session.execute(stmt)
        restaurant_db = res.fetchone()
        if not restaurant_db:
            raise ObjectDoesNotExistException(obj_name='restaurant', obj_id=id)

        await session.commit()

        restaurant_schema = RestaurnatSchema.model_validate(restaurant_db)
        return restaurant_schema
    
    async def create(
        self, create_data: RestaurantCreateSchema, session: AsyncSession
    ) -> RestaurnatSchema:
        data_dict: dict = jsonable_encoder(create_data, exclude_unset=True)

        await validate_unique(
            table=RestaurantTable,
            session=session,
            expressions_unique=(
                RestaurantTable.email == data_dict.get('email'),
                RestaurantTable.phone_number == data_dict.get('phone_number')
            ),
            unique_together=False
        )

        hashed_password: str = create_data.password + 'HS256'
        data_dict['password'] = hashed_password

        stmt = insert(RestaurantTable).values(**data_dict).returning('*')
        res = await session.execute(stmt)
        restaurant_db = res.fetchone()

        await session.commit()

        restaurant_schema = RestaurnatSchema.model_validate(restaurant_db)
        return restaurant_schema
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        await validate_restaurant_exist(id, session)

        stmt = delete(RestaurantTable).where(RestaurantTable.id == id)
        await session.execute(stmt)
        await session.commit()
        return None

        # # also delete related RestaurantAddress records
        # stmt_restaurant_address = (
        #     delete(RestaurantAddressTable)
        #     .where(RestaurantAddressTable.restaurant_id == id)
        # )
        # # also delete related Dish records
        # stmt_dish = delete(DishTable).where(DishTable.restaurant_id == id)
        # stmt_restaurant = delete(RestaurantTable).where(RestaurantTable.id == id)

        # async with session.begin():
        #     await session.execute(stmt_restaurant_address)
        #     await session.execute(stmt_dish)
        #     await session.execute(stmt_restaurant)
        #     await session.commit()
