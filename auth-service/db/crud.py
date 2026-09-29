from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

async def create_user(session: AsyncSession, email: str, password_hash: str, full_name: str) -> User:
    user = User(email=email, password=password_hash, full_name=full_name)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(
            select(User).where(User.email == email)
        )
    return result.scalar_one_or_none()