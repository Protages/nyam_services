from pydantic import BaseModel


class CustomerBaseSchema(BaseModel):
    email: str | None = None
    name: str | None = None


class CustomerUpdateSchema(CustomerBaseSchema):
    pass


class CustomerCreateSchema(CustomerBaseSchema):
    phone_number: str
    password: str


class CustomerSchema(CustomerBaseSchema):
    id: int
    phone_number: str
    password: str  # TODO: remove

    class Config:
        from_attributes = True
