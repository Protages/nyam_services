from pydantic import BaseModel, field_validator

from src.utils.validators import validate_password


class HashedPasswordInputSchema(BaseModel):
    row_password: str

    @field_validator('row_password')
    @classmethod
    def check_password(cls, v: str) -> str:
        errors: list[str] | None = validate_password(
            v, exclude_rule=['at_least_one_capital_letter']
        )
        if errors:
            raise ValueError(errors)
        return v


class HashedPasswordOutputSchema(BaseModel):
    hashed_password: str


class VerifyPasswordInputSchema(BaseModel):
    row_password: str
    hashed_password: str


class VerifyPasswordOutputSchema(BaseModel):
    is_verify: bool
