from app.worker.celery import celery_app
from loguru import logger
from collections import Counter
import redis
import json
from app.core.config import settings

# Создаем подключение к Redis для хранения счетчиков
redis_client = redis.Redis.from_url(settings.REDIS_URI)


@celery_app.task
def process_event_task(event_data: dict):
    """
    Фоновая задача для обработки события.
    """
    try:
        logger.info(f"Processing event: {event_data}")

        # Здесь будет сохранение в ClickHouse, отправка в Telegram и т.д.
        # Пока просто имитируем долгую обработку
        import time
        time.sleep(2)

        # Используем Counter для подсчета типов событий
        event_type = event_data.get('event_type', 'unknown')

        # Обновляем счетчик в Redis
        redis_client.hincrby('event_counts', event_type, 1)

        # Получаем актуальные счетчики
        event_counts = redis_client.hgetall('event_counts')
        decoded_counts = {k.decode('utf-8'): int(v) for k, v in event_counts.items()}

        logger.info(f"Event processed. Current counts: {decoded_counts}")

        return {"status": "success", "event_id": event_data.get("id")}
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {"status": "error", "error": str(e)}