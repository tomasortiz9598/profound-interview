from celery import Celery
from utils.settings import AppSettings

settings = AppSettings()

celery_app = Celery(
    "profound_interview",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["api.tasks"],
)
