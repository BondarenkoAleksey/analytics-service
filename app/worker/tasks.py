from app.worker.celery import celery_app
from loguru import logger


@celery_app.task
def process_event_task(event_data: dict):
    """
    Фоновая задача для обработки события.
    """
    # Пока просто логируем полученные данные
    logger.info(f"Processing event: {event_data}")

    # Здесь будет сохранение в ClickHouse, отправка в Telegram и т.д.
    # Пока просто имитируем долгую обработку
    import time
    time.sleep(3)

    logger.info(f"Event processed: {event_data}")
    return {"status": "success", "event_id": event_data.get("id")}
