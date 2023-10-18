from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    PasswordHashNotIdentifiedException,
    TokenCredentialsException,
    TokenExpiredException,
    TokenInvalidClaimsException,
)


def install_exception_handlers(app: FastAPI) -> None:
    '''Install all `exception handlers` by calling only this function.'''

    @app.exception_handler(PasswordHashNotIdentifiedException)
    async def password_hash_not_identified_exception_handler(
        request: Request, exc: PasswordHashNotIdentifiedException
    ):
        content = {'datail': exc.detail}
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(TokenCredentialsException)
    async def token_credentials_exception_handler(
        request: Request, exc: TokenCredentialsException
    ):
        content = {'datail': exc.detail}
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(TokenExpiredException)
    async def token_expired_exception_handler(
        request: Request, exc: TokenExpiredException
    ):
        content = {'datail': exc.detail}
        return JSONResponse(status_code=exc.status_code, content=content)
    
    @app.exception_handler(TokenInvalidClaimsException)
    async def token_invalid_claims_exception_handler(
        request: Request, exc: TokenInvalidClaimsException
    ):
        content = {'datail': exc.detail}
        return JSONResponse(status_code=exc.status_code, content=content)
