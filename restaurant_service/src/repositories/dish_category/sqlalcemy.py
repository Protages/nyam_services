from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete, select, insert
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.dish_category.abstract import DishCategoryAbcRepo
from src.schemas.dish import DishSchema
from src.schemas.dish_category import (
    DishCategoryCreateSchema,
    DishCategoryUpdateSchema,
    DishCategorySchema
)
from src.models.dish import DishCategoryTable, DishTable, dish_category_dish
from src.core.exceptions import ObjectDoesNotExistException
from src.utils.validators import validate_unique, validate_dish_category_exist


class DishCategorySQLAlchemyRepo(DishCategoryAbcRepo):
    async def get_by_id(
        self, id: int, session: AsyncSession
    ) -> DishCategorySchema:
        stmt = select(DishCategoryTable).where(DishCategoryTable.id == id)
        res = await session.execute(stmt)
        dish_category_db = res.fetchone()
        if not dish_category_db:
            raise ObjectDoesNotExistException(obj_name='dish', obj_id=id)

        dish_category_schema = DishCategorySchema.model_validate(dish_category_db[0])
        return dish_category_schema
    
    async def get_all(self, session: AsyncSession) -> list[DishCategorySchema]:
        stmt = select(DishCategoryTable)
        res = await session.execute(stmt)
        dish_categories_schema = [
            DishCategorySchema.model_validate(item[0])
            for item in res.fetchall()
        ]
        return dish_categories_schema
    
    async def get_dishes_by_dish_category(
        self, dish_category_id: int, session: AsyncSession
    ) -> list[DishSchema]:
        await validate_dish_category_exist(dish_category_id, session)

        # так достаем записи через связь M:M
        stmt = (
            select(DishTable)
            .select_from(dish_category_dish)
            .where(
                dish_category_dish.columns.get('dish_category_id')==dish_category_id, 
                DishTable.id==dish_category_dish.columns.get('dish_id')
            )
            .options(selectinload(DishTable.categories))
        )
        res = await session.execute(stmt)

        dish_schemas = [DishSchema.model_validate(dish[0]) for dish in res.fetchall()]
        return dish_schemas
    
    async def update(
        self, id: int, update_data: DishCategoryUpdateSchema, session: AsyncSession
    ) -> DishCategorySchema:
        data_dict: dict = jsonable_encoder(update_data, exclude_unset=True)

        await validate_unique(
            table=DishCategoryTable,
            session=session,
            expressions_unique=(
                DishCategoryTable.title == data_dict.get('title'),
            ),
            unique_together=False
        )

        # С помощью `returning` делаем апдейт + получаем обновленную запись одним запросом
        stmt = (
            update(DishCategoryTable)
            .where(DishCategoryTable.id == id)
            .values(data_dict)
            .returning('*')
        )
        res = await session.execute(stmt)
        dish_category_db = res.fetchone()
        if not dish_category_db:
            raise ObjectDoesNotExistException(obj_name='dish_category', obj_id=id)

        await session.commit()

        dish_category_schema = DishCategorySchema.model_validate(dish_category_db)
        return dish_category_schema
    
    async def create(
        self, create_data: DishCategoryCreateSchema, session: AsyncSession
    ) -> DishCategorySchema:
        data_dict: dict = jsonable_encoder(create_data, exclude_unset=True)

        await validate_unique(
            table=DishCategoryTable,
            session=session,
            expressions_unique=(
                DishCategoryTable.title == data_dict.get('title'),
            ),
            unique_together=False
        )

        stmt = insert(DishCategoryTable).values(**data_dict).returning('*')
        res = await session.execute(stmt)
        dish_category_db = res.fetchone()

        await session.commit()

        dish_category_schema = DishCategorySchema.model_validate(dish_category_db)
        return dish_category_schema
    
    async def delete(self, id: int, session: AsyncSession) -> None:
        await validate_dish_category_exist(id, session)

        stmt = (
            delete(DishCategoryTable)
            .where(DishCategoryTable.id == id)
        )

        async with session.begin():
            await session.execute(stmt)
            await session.commit()

        return None
