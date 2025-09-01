from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Схема для создания события (Запрос от клиента)
class EventCreate(BaseModel):
    # Pydantic автоматически проверяет типы и обязательность полей.
    event_type: str
    user_id: Optional[str] = None
    data: Optional[dict] = None
    comment: Optional[str] = None

    # Конфигурация для совместимости с ORM-объектами.
    # from_attributes=True позволяет использовать .model_validate(orm_obj)
    # для конвертации ORM -> Pydantic.
    model_config = ConfigDict(from_attributes=True)

# Схема для ответа с данными события (Ответ клиенту)
class EventResponse(EventCreate):
    # Добавляем поля, которые есть в БД, но не в запросе на создание.
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
