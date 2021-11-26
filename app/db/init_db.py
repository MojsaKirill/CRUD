from db.base import Base
from db.session import EngineAsync


async def init_models():
    async with EngineAsync.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
