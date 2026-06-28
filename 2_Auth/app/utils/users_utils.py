from sqlmodel import select

from app.models.Users import User
from app.core.db import db_session
from uuid import UUID


async def get_user_by_id(session: db_session, id: UUID) -> User | None:
    result = await session.exec(select(User).where(User.id == id))
    user = result.one_or_none()
    return user


async def get_user_by_username(session: db_session, username: str) -> User | None:
    result = await session.exec(select(User).where(User.username == username))
    user = result.one_or_none()
    return user