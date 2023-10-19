from fastapi import APIRouter

from src.api.http.routes import check_services, courier, login


prefix = '/api/v1'

api_router = APIRouter(prefix=prefix)
api_router.include_router(courier.router)
api_router.include_router(login.router)
api_router.include_router(check_services.router)
