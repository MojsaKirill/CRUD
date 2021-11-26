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
