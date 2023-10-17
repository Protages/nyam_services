from pydantic import BaseModel


class DishCategoryDishSchema(BaseModel):
    dish_id: int
    dish_category_id: int
