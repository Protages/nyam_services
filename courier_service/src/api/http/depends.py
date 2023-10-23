from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.services.courier import CourierService
from src.schemas.login import TokenPayloadOutputSchema
from src.utils.auth import verify_token_and_get_payload
from src.utils.uow.sqlalchemy import UOWSQLAlchemy


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def courier_service() -> CourierService:
    '''CourierService with `UOWSQLAlchemy` for work with SQLAlchemy ORM.'''
    return CourierService(UOWSQLAlchemy)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload: TokenPayloadOutputSchema = verify_token_and_get_payload(token)
    return payload
