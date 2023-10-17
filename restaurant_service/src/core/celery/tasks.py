import os

import httpx
from celery import Celery


celery = Celery('celery_restaurant')
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task
def get_customer_service_info(url: str):
    print('------- start celere task')
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    response: httpx.Response = httpx.get(url, headers=headers)
    print('------', response)
