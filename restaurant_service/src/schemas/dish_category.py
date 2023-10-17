from pydantic import BaseModel


class DishCategoryBaseSchema(BaseModel):
    title: str | None = None


class DishCategoryUpdateSchema(DishCategoryBaseSchema):
    pass


class DishCategoryCreateSchema(DishCategoryBaseSchema):
    title: str


class DishCategorySchema(BaseModel):
    id: int
    title: str | None = None

    class Config:
        from_attributes = True
