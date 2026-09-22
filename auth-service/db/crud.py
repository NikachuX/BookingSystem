from sqlalchemy import select

from .database import AsyncSessionLocal
from .models import User

async def create_user(session: AsyncSessionLocal, email: str, password_hash: str, full_name: str) -> User:
    user = User(email=email, password=password_hash, full_name=full_name)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_email(session: AsyncSessionLocal, email: str) -> User | None:
    result = await session.execute(
            select(User).where(User.email == email)
        )
    return result.scalar_one_or_none()