from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# create_async_engine создает "движок" - точку входа в БД, которая управляет подключениями.
# Параметры:
# echo=True - очень полезно при разработке, будет логировать все SQL-запросы в консоль.
# pool_size, max_overflow - настройки пула соединений.
# engine = create_async_engine(
#     settings.SQLALCHEMY_DATABASE_URI,
#     echo=True,  # В продакшене обычно False
#     future=True,  # Всегда используем будущее API SQLAlchemy 2.0
# )
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),  # Явное преобразование в строку
    echo=True,
    future=True
)

# async_sessionmaker - это фабрика для создания асинхронных сессий.
# Сессия - это основной объект, через который происходят все взаимодействия с БД.
# expire_on_commit=False - важная настройка. После коммита объекты в сессии не становятся "недействительными",
# что позволяет продолжать с ними работать (например, вернуть их из эндпоинта в ответе).
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Важная функция-зависимость (Dependency) для FastAPI.
# Она будет вызываться для каждого запроса, создавая новую сессию,
# и гарантированно закрывать ее после обработки запроса, даже если произошла ошибка.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Сессия передается в эндпоинт
            await session.commit()  # Если все хорошо - коммитим транзакцию
        except Exception:
            await session.rollback()  # Если ошибка - откатываем
            raise
        finally:
            await session.close()  # Всегда закрываем сессию
