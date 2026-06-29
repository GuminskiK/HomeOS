from datetime import timedelta

from sqlmodel import select
from structlog.contextvars import bind_contextvars
from app.utils.auth_utils import get_password_hash
from app.core.config import settings
from app.core.exceptions import (
    UsernameTakenException,
    UserNotFoundException,
)
from uuid import UUID

from app.models.Users import User, UserCreate, UserUpdate
from app.utils.users_utils import get_user_by_id, get_user_by_username
from app.core.db import db_session
from common.logger import get_logger

logger = get_logger(__name__)

async def create_user(
        session: db_session,
        user: UserCreate
):
    if await get_user_by_username(session, user.username):
        logger.warning("user_create_failed_username_taken")
        raise UsernameTakenException()
    
    hashed = get_password_hash(user.plain_password)
    user_data = user.model_dump(exclude={"plain_password"})
    db_user = User(
        **user_data, hashed_password=hashed
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    logger.info("user_created_succesfully", user_id=db_user.id)
    
    return db_user

async def fetch_user_by_id(
    session: db_session, 
    user_id: UUID
) -> User:
    
    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_fetch_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    return user

async def fetch_all_users(session: db_session) -> list[User]:
    result = await session.exec(select(User))
    users = list(result.all())
    return users

async def update_user(
    session: db_session, 
    user_id: UUID, 
    user_update: UserUpdate
) -> User:

    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_update_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    
    if user_update.plain_password:
        hashed = get_password_hash(user_update.plain_password)
        user_update.hashed_password = hashed
    
    update_data = user_update.model_dump(exclude_unset=True, exclude={"plain_password"})
    for key, value in update_data.items():
        setattr(user, key, value)
    
    session.add(user)
    await session.commit()
    await session.refresh(user)

    logger.info("user_updated_succesfully", user_id=user.id)
    
    return user

async def remove_user(session: db_session, user_id: UUID):
    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_remove_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    
    await session.delete(user)
    await session.commit()

    logger.info("user_removed_succesfully", user_id=user.id)

    return {"message": "User removed successfully"}