from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

Base = declarative_base()

EngineAsync = create_async_engine(settings.SQLALCHEMY_DATABASE_URL,
                                  pool_pre_ping=True,
                                  echo=settings.DEBUG,
                                  future=settings.FUTURE,
                                  connect_args={'check_same_thread': False})

SessionAsync = sessionmaker(EngineAsync,
                            class_=AsyncSession,
                            expire_on_commit=False)

# https://t.me/fastapi_ru/30947
# def session_getter(db_url: str, echo: bool):
#     engine = create_async_engine(db_url, pool_pre_ping=True, echo=echo, future=True,
#                                  connect_args={'check_same_thread': False})
#     Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#
#     async def get_db_session() -> AsyncSession:
#         db = Session()
#         try:
#             yield db
#         finally:
#             await db.close()
#
#     return get_db_session
