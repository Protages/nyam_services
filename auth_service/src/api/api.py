from fastapi import APIRouter

from src.api.routes import check_services, password, token


prefix = '/api/v1'

api_router = APIRouter(prefix=prefix)
api_router.include_router(check_services.router)
api_router.include_router(password.router)
api_router.include_router(token.router)
