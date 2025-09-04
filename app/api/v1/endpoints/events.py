from alembic.util import status
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.event import EventRepository
from app.db.session import get_db
from app.models.pydantic.event import EventCreate, EventResponse
from app.worker.tasks import process_event_task


router = APIRouter()

@router.get("/health")
async def health_check() -> dict:
    return {"status": "OK"}

# @router.post("/", response_model=EventCreate)
@router.post("/", response_model=EventResponse)
async def create_event(
        event_data: EventCreate,
        db: AsyncSession = Depends(get_db),
) -> EventResponse:
    """
    Create a new analytics event.
    """
    repo = EventRepository(session=db)
    new_event = await repo.create(event_create=event_data)
    await db.refresh(new_event)


    # Отправляем задачу в Celery для фоновой обработки
    process_event_task.delay(new_event.to_dict())
    return new_event
