from typing import Literal

from pydantic import BaseModel

from src.schemas.password import VerifyPasswordInputSchema, VerifyPasswordOutputSchema


UserTypes = Literal['customer', 'restaurnat', 'courier']


class GetTokenInputSchema(BaseModel):
    user_id: int
    user_type: UserTypes


class GetTokenOutputSchema(BaseModel):
    token: str
    token_type: str


class VerifyPasswordAndGetTokenInputSchema(
    VerifyPasswordInputSchema,
    GetTokenInputSchema
):
    pass


class VerifyPasswordAndGetTokenOutputSchema(
    VerifyPasswordOutputSchema,
    GetTokenOutputSchema
):
    pass


class VerifyTokenInputSchema(BaseModel):
    token: str


class VerifyTokenOutputSchema(GetTokenInputSchema):
    pass
