import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.environ.get('ENV_FILE'), 
        env_file_encoding='utf-8'
    )

    # Services urls
    CUSTOMER_SERVICE_URL: str = 'http://127.0.0.1:8001/'
    RESTAURANT_SERVICE_URL: str = 'http://127.0.0.1:8002/'
    COURIER_SERVICE_URL: str = 'http://127.0.0.1:8003/'
    ORDER_SERVICE_URL: str = 'http://127.0.0.1:8004/'
    AUTH_SERIVICE_URL: str = 'http://127.0.0.1:8005/'
    NOTIFICATION_SERVICE_URL: str = 'http://127.0.0.1:8006/'

    # JWT token
    SECKET_KEY: str = '4b42c95007644afae6d74c9df95a5b5829200e130dfad17bbbf0d59230a16484'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TYPE: str = 'Bearer'


@lru_cache
def get_settigns() -> Settings:
    return Settings()


settings = get_settigns()
