from contextlib import asynccontextmanager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.exceptions import DBOperationError

Base = declarative_base()


class SessionManager:

    def __init__(self):
        self._session_factory = sessionmaker(
            bind=create_async_engine(
                settings.SQLALCHEMY_DATABASE_URL,
                pool_pre_ping=True,
                echo=settings.DEBUG,
                future=settings.FUTURE,
                connect_args={'check_same_thread': False},
            ),
            class_=AsyncSession,
            expire_on_commit=False,
            future=settings.FUTURE,
        )

    @asynccontextmanager
    async def obtain_session(self) -> AsyncSession:
        session = self._session_factory()
        try:
            yield session
            await session.commit()
        except BaseException as e:
            await session.rollback()
            raise DBOperationError(f'Error: {e}')
        finally:
            await session.close()
