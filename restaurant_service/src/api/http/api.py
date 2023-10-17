from fastapi import APIRouter

from src.api.http.routes import (
    check_services,
    dish,
    dish_category,
    restaurant,
    restaurant_address
)


prefix = '/api/v1'

api_router = APIRouter()
api_router.include_router(restaurant.router, prefix=prefix)
api_router.include_router(restaurant_address.router, prefix=prefix)
api_router.include_router(dish.router, prefix=prefix)
api_router.include_router(dish_category.router, prefix=prefix)
api_router.include_router(check_services.router, prefix=prefix)
