import asyncio
from .database import engine, Base
from .models import User

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
