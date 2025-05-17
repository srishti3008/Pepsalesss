from celery import Celery
from .settings import settings

celery_app = Celery(
    "notifier",
    broker=settings.RABBITMQ_BROKER,
    backend="rpc://",
)

celery_app.conf.task_routes = {"app.tasks.*": {"queue": "notifications"}}