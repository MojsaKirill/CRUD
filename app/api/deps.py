from sqlalchemy.ext.asyncio import AsyncSession

from db.session import SessionAsync


async def get_session() -> AsyncSession:
    async with SessionAsync() as session:
        yield session
