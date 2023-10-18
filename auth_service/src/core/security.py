from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import ExpiredSignatureError, JWTError, jwt

from src.schemas.token import VerifyTokenOutputSchema
from src.core.config import settings
from src.core.exceptions import (
    PasswordHashNotIdentifiedException,
    TokenCredentialsException,
    TokenExpiredException,
    TokenInvalidClaimsException
)


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(row_password: str) -> str:
    '''Hashing row passwrod. Each time will be different hash on the same password!'''
    return pwd_context.hash(row_password)


def is_verify_password(row_password: str, hashed_password: str) -> bool:
    try:
        is_verify = pwd_context.verify(row_password, hashed_password)
    except ValueError:
        raise PasswordHashNotIdentifiedException
    return is_verify


def get_token(data_to_encode: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data_to_encode.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.SECKET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> VerifyTokenOutputSchema:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECKET_KEY,
            algorithms=settings.ALGORITHM
        )
        user_id: int = payload.get('user_id')
        user_type: str = payload.get('user_type')
        if user_id is None or user_type is None:
            raise TokenInvalidClaimsException
        token_schema = VerifyTokenOutputSchema(user_id=user_id, user_type=user_type)

    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise TokenCredentialsException

    return token_schema
