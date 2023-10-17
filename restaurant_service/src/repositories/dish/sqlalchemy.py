from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, select, insert, Insert
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm.collections import InstrumentedList

from src.repositories.dish.abstract import DishAbcRepo
from src.schemas.dish import (
    DishCreateSchema,
    DishUpdateSchema,
    DishSchema
)
from src.schemas.dish_category_dish import DishCategoryDishSchema
from src.models.dish import DishTable, DishCategoryTable, dish_category_dish
from src.core.exceptions import ObjectDoesNotExistException
from src.utils.validators import validate_unique, validate_dish_exist, validate_dish_category_exist


class DishSQLAlchemyRepo(DishAbcRepo):
    async def __insert_dish_category_dish(
        self, session: AsyncSession, dish_id: int, categories_id: list[int]
    ) -> None:
        dish_category_dish_data: list[dict] = []
        for cat_id in categories_id:
            category_db = await validate_dish_category_exist(cat_id, session)
            dish_category_dish_data.append(DishCategoryDishSchema(
                dish_id=dish_id,
                dish_category_id=category_db.id
            ).model_dump())

        cat_stmt = insert(dish_category_dish).values(dish_category_dish_data)
        await session.execute(cat_stmt)

    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> DishSchema:
        stmt = (
            select(DishTable)
            .where(DishTable.id == id)
            .options(selectinload(DishTable.categories))
        )
        res = await session.execute(stmt)
        dish_db = res.fetchone()
        if not dish_db:
            raise ObjectDoesNotExistException(obj_name='dish', obj_id=id)
        
        dish_schema = DishSchema.model_validate(dish_db[0])
        return dish_schema
    
    async def get_all(self, session: AsyncSession) -> list[DishSchema]:
        stmt = select(DishTable).options(selectinload(DishTable.categories))
        res = await session.execute(stmt)
        dishes_schema = [
            DishSchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return dishes_schema
    
    async def update(
        self, id: int, update_data: DishUpdateSchema, session: AsyncSession
    ) -> DishSchema:
        data_dict: dict = jsonable_encoder(
            update_data, exclude_unset=True, exclude=('categories',)
        )

        # TODO: нужно сделать проверку на уникальность title и restaurant_id!

        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        if data_dict:
            stmt = (
                update(DishTable)
                .where(DishTable.id == id)
                .values(data_dict)
                .returning('*')
            )
        else:
            stmt = (
                select(DishTable)
                .where(DishTable.id == id)
            )

        res = await session.execute(stmt)
        dish_db = res.fetchone() if data_dict else res.scalar_one()

        if not dish_db:
            raise ObjectDoesNotExistException(obj_name='dish', obj_id=id)
        
        if update_data.categories:
            # before create new many to many records, delete old

            # old sync version
            # old_categories: InstrumentedList = dish_db.categories
            # old_categories.clear()

            # new 2.0 style async version
            cat_delete_old_stmt = (
                delete(dish_category_dish)
                .where(dish_category_dish.columns.get('dish_id') == id)
            )
            await session.execute(cat_delete_old_stmt)

            await self.__insert_dish_category_dish(
                session, id, update_data.categories
            )

        await session.commit()

        updated_dish_stmt = (
            select(DishTable)
            .where(DishTable.id == id)
            .options(selectinload(DishTable.categories))
        )
        updated_dish_res = await session.execute(updated_dish_stmt)
        updated_dish_db = updated_dish_res.scalar_one()

        dish_schema = DishSchema.model_validate(updated_dish_db)
        return dish_schema
    
    async def create(
        self, create_data: DishCreateSchema, session: AsyncSession
    ) -> DishSchema:
        data_dict: dict = jsonable_encoder(
            create_data, exclude_unset=True, exclude=('categories',)
        )

        await validate_unique(
            table=DishTable,
            session=session,
            expressions_unique=(
                DishTable.title == create_data.title,
                DishTable.restaurant_id == create_data.restaurant_id
            ),
            unique_together=True
        )

        stmt = insert(DishTable).values(**data_dict).returning('*')
        res = await session.execute(stmt)
        dish_db = res.fetchone()
        dish_id: int = dish_db.id

        if create_data.categories:
            await self.__insert_dish_category_dish(
                session, dish_id, create_data.categories
            )

        await session.commit()

        created_dish_stmt = (
            select(DishTable)
            .where(DishTable.id == dish_id)
            .options(selectinload(DishTable.categories))
        )
        created_dish_res = await session.execute(created_dish_stmt)
        created_dish_db = created_dish_res.scalar_one()

        dish_schema = DishSchema.model_validate(created_dish_db)
        return dish_schema
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        stmt = (
            delete(DishTable)
            .where(DishTable.id == id)
        )
        res = await session.execute(stmt)

        if not res.rowcount:
            raise ObjectDoesNotExistException(obj_name='dish', obj_id=id)

        await session.commit()
        return
