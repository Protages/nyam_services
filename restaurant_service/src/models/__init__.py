# Import tables need for alembic migration work.

from src.models.restaurant import RestaurantTable, RestaurantAddressTable  # noqa: F401
from src.models.dish import DishTable, DishCategoryTable, dish_category_dish  # noqa: F401
from src.database.db import Base  # noqa: F401
