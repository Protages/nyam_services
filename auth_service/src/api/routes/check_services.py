import httpx

from fastapi import APIRouter, status

from src.schemas.check_service import CheckServiceResponseSchema
from src.core.config import settings


router = APIRouter(tags=['Check Services'])


@router.get('/service_working') 
async def service_working() -> dict:
    return {'message': 'Hello from auth service!'}


async def __check_service_working(url: str) -> CheckServiceResponseSchema:
    '''Common method for check another service working.'''
    try:
        response: httpx.Response = httpx.get(url)

        return CheckServiceResponseSchema(
            response=response.json(), 
            status_code=response.status_code, 
            request_timedelta=response.elapsed
        )
    except httpx.ConnectError:
        return CheckServiceResponseSchema(
            response={'error': 'Service not allowed.'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get('/check/customer', response_model=CheckServiceResponseSchema)
async def check_customer_service_working():
    url = f'{settings.CUSTOMER_SERVICE_URL}api/v1/service_working'
    return await __check_service_working(url)


@router.get('/check/restaurant', response_model=CheckServiceResponseSchema)
async def check_courier_service_working():
    url = f'{settings.RESTAURANT_SERVICE_URL}api/v1/service_working'
    return await __check_service_working(url)


@router.get('/check/courier', response_model=CheckServiceResponseSchema)
async def check_auth_service_working():
    url = f'{settings.COURIER_SERVICE_URL}api/v1/service_working'
    return await __check_service_working(url)


@router.get('/check/order', response_model=CheckServiceResponseSchema)
async def check_order_service_working():
    url = f'{settings.ORDER_SERVICE_URL}api/v1/service_working'
    return await __check_service_working(url)


@router.get('/check/notification', response_model=CheckServiceResponseSchema)
async def check_notification_service_working():
    url = f'{settings.NOTIFICATION_SERVICE_URL}api/v1/service_working'
    return await __check_service_working(url)
