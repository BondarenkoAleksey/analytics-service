from fastapi import FastAPI
from app.core.config import settings

from app.api.v1.endpoints import events, reports
from app.db.session import engine
from app.models.sqlalchemy.base import Base

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])

@app.on_event("startup")
async def startup_event():
    # Создаем таблицы. В продакшене используй Alembic!
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
