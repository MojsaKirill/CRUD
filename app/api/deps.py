from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import SessionLocal, async_session


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
