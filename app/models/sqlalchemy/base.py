from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime

# Современный стиль объявления моделей для SQLAlchemy 2.0
class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовая модель для всех ORM-моделей.
    AsyncAttrs добавляет асинхронный доступ к отложенно загруженным атрибутам.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Автоматически генерирует имя таблицы из имени класса в lower case.
        return cls.__name__.lower()

    # Общие поля для всех таблиц
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )