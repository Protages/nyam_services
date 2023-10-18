from pydantic import BaseModel


class CourierBaseSchema(BaseModel):
    email: str | None = None
    name: str | None = None
    is_work: bool | None = None
    is_free: bool | None = None
    photo: str | None = None


class CourierUpdateSchema(CourierBaseSchema):
    pass


class CourierCreateSchema(CourierBaseSchema):
    phone_number: str
    password: str
    name: str


class CourierSchema(CourierBaseSchema):
    id: int
    phone_number: str
    password: str  # TODO: remove!

    class Config:
        from_attributes = True


class CourierForGetTokenSchema(BaseModel):
    id: int
    password: str

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    phone_number: str
    password: str


class TokenSchema(BaseModel):
    token: str
    token_type: str
