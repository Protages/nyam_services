from pydantic import BaseModel


class LoginSchema(BaseModel):
    phone_number: str
    password: str


class TokenSchema(BaseModel):
    token: str
    token_type: str


class CourierForGetTokenSchema(BaseModel):
    id: int
    password: str

    class Config:
        from_attributes = True


class TokenPayloadOutputSchema(BaseModel):
    user_id: int
    user_type: str
