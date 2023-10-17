from pydantic import BaseModel, field_serializer, Field

from src.schemas.dish_category import DishCategorySchema


class DishBaseSchema(BaseModel):
    title: str | None = None
    price: int | None = None
    in_stock: bool | None = None
    visible: bool | None = None
    image: str | None = None
    categories: list[int] | None = None


class DishUpdateSchema(DishBaseSchema):
    pass


class DishCreateSchema(DishBaseSchema):
    title: str
    price: int
    restaurant_id: int


class DishSchema(DishBaseSchema):
    id: int
    restaurant_id: int
    categories: list[DishCategorySchema] | None = None

    class Config:
        from_attributes = True
