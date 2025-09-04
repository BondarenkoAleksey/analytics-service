from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn, AmqpDsn, validator
from typing import Optional


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "Analytics Service API"
    DEBUG: bool = False

    # Database (PostgreSQL для основных данных)
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5433
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # Валидатор: автоматически собирает DSN строку из отдельных полей
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg", # Используем асинхронный драйвер
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # ClickHouse для аналитики (отдельный валидатор можно добавить)
    CLICKHOUSE_SERVER: str = "localhost"
    CLICKHOUSE_DB: str = "analytics"

    # Redis для кеша и Celery broker/backend
    REDIS_URI: str

    # RabbitMQ для сообщений (aio-pika)
    RABBITMQ_URI: AmqpDsn

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: Optional[str] = None

    # Класс Config говорит pydantic, где искать .env файл.
    class Config:
        env_file = ".env"
        case_sensitive = True

# Создаем инстанс настроек, который будем импортировать по всему проекту
settings = Settings()
