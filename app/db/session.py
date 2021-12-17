from contextlib import asynccontextmanager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import init_logging, settings
from core.exceptions import DBOperationError

logger = init_logging(__name__)

Base = declarative_base()


class SessionManager:

    def __init__(self):
        self._session_factory = sessionmaker(
            bind=create_async_engine(
                settings.SQLALCHEMY_DATABASE_URL_ASYNC,
                pool_pre_ping=True,
                echo=settings.DEBUG,
                future=settings.FUTURE,
            ),
            class_=AsyncSession,
            expire_on_commit=False,
            future=settings.FUTURE,
        )

    @asynccontextmanager
    async def obtain_session(self) -> AsyncSession:
        logger.debug('Create session...')
        session = self._session_factory()
        logger.debug('Session created...')
        try:
            logger.debug('Run statement...')
            yield session
            logger.debug('Committing...')
            await session.commit()
            logger.debug('Committed.')
        except Exception as e:
            logger.error('Obtain session: failed')
            logger.exception(e)
            logger.debug('Rollback transaction...')
            await session.rollback()
            logger.debug('Rollback done.')
            raise DBOperationError(e)
        finally:
            logger.debug('Closing connection...')
            await session.close()
            logger.debug('Connection closed.')
