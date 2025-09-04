from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON, Text
from app.models.sqlalchemy.base import Base

class Event(Base):
    """
    Модель для хранения событий.
    """

    # Переопределяем имя таблицы, если нужно (опционально)
    __tablename__ = "events"

    # Тип события (e.g., 'user_signup', 'purchase', 'page_view')
    # Index=True ускоряет поиск и агрегацию по этому полю.
    event_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)

    # Идентификатор пользователя (может быть NULL для анонимных событий)
    user_id: Mapped[str | None] = mapped_column(String(50), index=True)

    # Произвольные данные события в формате JSON.
    # Важно: Для PostgreSQL лучше использовать тип JSONB, он эффективнее.
    # Для других СУБД (MySQL) используем JSON.
    data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Дополнительное текстовое поле для демонстрации или хранения неструктурированных данных.
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "data": self.data,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
