from pydantic import BaseModel, EmailStr, Field


class RestaurantBaseSchema(BaseModel):
    email: str | None = None
    title: str | None = None
    description: str | None = None
    icon: str | None = None
    is_open: bool | None = None


class RestaurantUpdateSchema(RestaurantBaseSchema):
    pass


class RestaurantCreateSchema(RestaurantBaseSchema):
    phone_number: str
    password: str
    email: str
    title: str
    is_open: bool = False


class RestaurnatSchema(RestaurantBaseSchema):
    id: int
    phone_number: str
    password: str  # TODO: remove

    class Config:
        from_attributes = True
