from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    AnotherServiceException,
    PasswordInvalidException,
    ObjectDoesNotExistException,
    UniqueFailedException,
)


def install_exception_handlers(app: FastAPI) -> None:
    '''Install all `exception handlers` by calling only this function.'''

    @app.exception_handler(AnotherServiceException)
    async def another_service_exception_handler(
        request: Request, exc: AnotherServiceException
    ):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(PasswordInvalidException)
    async def password_invalid_exception_handler(
        request: Request, exc: PasswordInvalidException
    ):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(ObjectDoesNotExistException)
    async def object_does_not_exist_exception_handler(
        request: Request, exc: ObjectDoesNotExistException
    ):
        content = f'{exc.obj_name.capitalize()} with id <{exc.obj_id}> does not exist.'
        if not exc.obj_id:
            content = f'{exc.obj_name.capitalize()} does not exist.'
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)

    @app.exception_handler(UniqueFailedException)
    async def unique_failed_exception_handler(
        request: Request, exc: UniqueFailedException
    ):
        # if True then is unique_together exception
        if isinstance(exc.fields_name, (tuple, list)):
            fields_name = ' and '.join(f'<{key}>' for key in exc.fields_name)
            content = f'Values of fields {fields_name} must be unique together.'
        else:
            content = f'Value of field <{exc.fields_name}> must be unique.'
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
