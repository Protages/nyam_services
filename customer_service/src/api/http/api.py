from fastapi import APIRouter

from src.api.http.routes import check_services, customer, customer_address


prefix = '/api/v1'

api_router = APIRouter()
api_router.include_router(customer.router, prefix=prefix)
api_router.include_router(customer_address.router, prefix=prefix)
api_router.include_router(check_services.router, prefix=prefix)
