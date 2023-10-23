import httpx
from fastapi import HTTPException, status


class AnotherServiceException(HTTPException):
    '''Exception to raise when another microservice raises exception.'''

    def __init__(self, response: httpx.Response) -> None:
        super().__init__(response.status_code, response.json())


class ObjectDoesNotExistException(Exception):
    def __init__(
        self, obj_name: str | None = 'object', obj_id: int | None = None
    ) -> None:
        self.obj_name = obj_name
        self.obj_id = obj_id


class UniqueFailedException(Exception):
    def __init__(self, fields_name: str | tuple | list) -> None:
        '''
        If `field_name` is `tuple`, then consider it as unique_together exception.
        '''
        self.fields_name = fields_name
