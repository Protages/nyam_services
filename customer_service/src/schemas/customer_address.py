from pydantic import BaseModel


class CustomerAddressBaseSchema(BaseModel):
    address: str | None = None
    geolocation: str | None = None
    title: str | None = None
    icon: str | None = None


class CustomerAddressUpdateSchema(CustomerAddressBaseSchema):
    pass


class CustomerAddressCreateSchema(CustomerAddressBaseSchema):
    address: str
    customer_id: int


class CustomerAddressSchema(CustomerAddressBaseSchema):
    id: int
    customer_id: int

    class Config:
        from_attributes = True
