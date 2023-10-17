from sqlalchemy import exists, select, Column
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.elements import BinaryExpression

from src.database.db import Base
from src.models.restaurant import RestaurantTable, RestaurantAddressTable
from src.models.dish import DishTable, DishCategoryTable
from src.core.exceptions import ObjectDoesNotExistException, UniqueFailedException


async def validate_exist(
    id: int,
    table: DeclarativeMeta,
    session: AsyncSession,
    obj_name: str,
    pk_name: str = 'id'
) -> Base | ObjectDoesNotExistException:
    stmt = select(table).filter(getattr(table, pk_name) == id)
    res = await session.execute(stmt)
    instance_db = res.scalar()

    if not instance_db:
        raise ObjectDoesNotExistException(obj_name=obj_name, obj_id=id)
    return instance_db


async def validate_restaurant_exist(
    id: int, session: AsyncSession
) -> RestaurantTable | ObjectDoesNotExistException:
    '''
    Check that Restaurant with passed `id` exist,
    else raise `ObjectDoesNotExistException`.
    '''
    return await validate_exist(id, RestaurantTable, session, 'restaurant')


async def validate_restaurant_address_exist(
    id: int, session: Session
) -> RestaurantAddressTable | ObjectDoesNotExistException:
    '''
    Check that RestaurantAddress with passed `id` exist,
    else raise `ObjectDoesNotExistException`.
    '''
    return await validate_exist(id, RestaurantAddressTable, session, 'restaurant_address')


async def validate_dish_exist(
    id: int, session: Session
) -> DishTable | ObjectDoesNotExistException:
    '''
    Check that Dish with passed `id` exist,
    else raise `ObjectDoesNotExistException`.
    '''
    return await validate_exist(id, DishTable, session, 'dish')


async def validate_dish_category_exist(
    id: int, session: Session
) -> DishCategoryTable | ObjectDoesNotExistException:
    '''
    Check that DishCategory with passed `id` exist,
    else raise `ObjectDoesNotExistException`.
    '''
    return await validate_exist(id, DishCategoryTable, session, 'dish_category')


async def validate_unique(
    table: DeclarativeMeta | str,
    session: AsyncSession,
    expressions_unique: tuple[BinaryExpression],
    unique_together: bool = False
) -> None | UniqueFailedException:
    '''
    If send more `expressions_unique`, there will be check for unique together

    :param expressions_unique: 
        tuple of unique expressions for WHERE operator/operators.
    :param unique_together: 
        If `True` then ALL exp from expressions_unique will be in one WHERE operator, 
        if `False` then on EACH exp from expressions_unique will be one WHERE operator.
    '''
    if unique_together:
        stmt = select(table).where(*expressions_unique)
        res = await session.execute(stmt)
        is_exist = res.scalar()
        if is_exist:
            unique_keys = [ex.left.key for ex in expressions_unique]
            raise UniqueFailedException(unique_keys)
    else:
        for exp in expressions_unique:
            stmt = select(table).where(exp)
            res = await session.execute(stmt)
            is_exist = res.scalar()
            if is_exist:
                raise UniqueFailedException(exp.left.key)
