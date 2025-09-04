from celery import Celery
from app.core.config import settings

# Создаем экземпляр Celery, указываем брокер (Redis) и бэкенд (Redis для результатов)
celery_app = Celery(
    "worker",
    broker=str(settings.REDIS_URI),
    backend=str(settings.REDIS_URI),
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# Автоматически обнаруживаем задачи в модуле app.worker.tasks
celery_app.autodiscover_tasks(["app.worker.tasks"])