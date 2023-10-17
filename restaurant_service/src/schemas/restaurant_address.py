from pydantic import BaseModel


class RestaurantAddressBaseSchema(BaseModel):
    address: str | None = None
    geolocation: str | None = None
    title: str | None = None


class RestaurantAddressUpdateSchema(RestaurantAddressBaseSchema):
    pass


class RestaurantAddressCreateSchema(RestaurantAddressBaseSchema):
    address: str
    restaurant_id: int


class RestaurantAddressSchema(RestaurantAddressBaseSchema):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True
