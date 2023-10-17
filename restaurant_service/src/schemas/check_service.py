import datetime

from pydantic import BaseModel


class CheckServiceResponseSchema(BaseModel):
    response: str | dict
    status_code: int
    request_timedelta: datetime.timedelta | None = None
