from src.repositories.restaurant.sqlalchemy import RestaurantSQLAlchemyRepo
from src.repositories.restaurant_address.sqlalchemy import RestaurantAddressSQLAlchemyRepo
from src.repositories.dish.sqlalchemy import DishSQLAlchemyRepo
from src.repositories.dish_category.sqlalcemy import DishCategorySQLAlchemyRepo
from src.services.restaurant import RestaurantService
from src.services.restaurant_address import RestaurantAddressService
from src.services.dish import DishService
from src.services.dish_category import DishCategoryService


def restaurant_service():
    '''Return RestaurantService with `RestaurantSQLAlchemyRepo`.'''
    return RestaurantService(RestaurantSQLAlchemyRepo)


def restaurant_address_service():
    '''Return RestaurantAddressService with `RestaurantAddressSQLAlchemyRepo`.'''
    return RestaurantAddressService(RestaurantAddressSQLAlchemyRepo)


def dish_service():
    '''Return DishService with `DishSQLAlchemyRepo`.'''
    return DishService(DishSQLAlchemyRepo)


def dish_category_service():
    '''Return DishCategoryService with `DishCategorySQLAlchemyRepo`.'''
    return DishCategoryService(DishCategorySQLAlchemyRepo)


# from src.database.db import SessionLocal
# def get_session():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
