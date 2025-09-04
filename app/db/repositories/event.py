from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sqlalchemy.event import Event
from app.models.pydantic.event import EventCreate

class EventRepository:
    """Репозиторий для операций CRUD с событиями."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event_create: EventCreate) -> Event:
        """
        Создает и сохраняет новое событие в БД.
        Args:
            event_create: Схема Pydantic с данными для создания.
        Returns:
            ORM-объект Event.
        """
        # Создаем экземпляр ORM-модели из данных Pydantic-схемы.
        db_event = Event(**event_create.model_dump())

        # Добавляем его в сессию
        self.session.add(db_event)

        # ✅ Сохраняем изменения в базе
        await self.session.commit()

        # ✅ Обновляем объект из базы, чтобы все поля (id, timestamps и т.д.) были доступны
        await self.session.refresh(db_event)

        return db_event

    async def get_by_id(self, event_id: int) -> Event | None:
        """Получает событие по его ID."""
        result = await self.session.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none()

    # Здесь позже добавятся методы get_multi, get_by_type, etc.
