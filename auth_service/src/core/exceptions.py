from fastapi import status, HTTPException


class PasswordHashNotIdentifiedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Password hash could not be identified'
        )


class PasswordInvalidException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail='Invalid password')


class TokenCredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )


class TokenExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Signature has expired'
        )


class TokenInvalidClaimsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token payload'
        )
