import os
from functools import lru_cache

# from pydantic import EmailStr, HttpUrl
from pydantic_settings import BaseSettings

from config import ASYNC_SQLITE_URL as BASE_ASYNC_SQLITE_URL


class Settings(BaseSettings):
    # Services urls
    CUSTOMER_SERVICE_URL: str = 'http://127.0.0.1:8001/'
    RESTAURANT_SERVICE_URL: str = 'http://127.0.0.1:8002/'
    COURIER_SERVICE_URL: str = 'http://127.0.0.1:8003/'
    ORDER_SERVICE_URL: str = 'http://127.0.0.1:8004/'
    AUTH_SERIVICE_URL: str = 'http://127.0.0.1:8005/'
    NOTIFICATION_SERVICE_URL: str = 'http://127.0.0.1:8006/'

    # Logger
    QUERY_LOGGER: bool = True

    # SQLite
    USE_SQLITE: bool = True
    ASYNC_SQLITE_URL: str = BASE_ASYNC_SQLITE_URL

    # class Config:
    #     env_file = os.environ.get('ENV_FILE', '.env.dev')


@lru_cache
def get_settigns() -> Settings:
    return Settings()


settings = get_settigns()
