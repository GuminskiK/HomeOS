import shutil
from pathlib import Path as FilePath
from fastapi import File, UploadFile
from sqlmodel import select
from app.utils.auth_utils import get_password_hash
from app.core.exceptions import (
    NoFileNameException,
    NoFileTypeException,
    UsernameTakenException,
    UserNotFoundException,
    WrongFileTypeException,
    NoFileException
)
from uuid import UUID, uuid4

from app.models.Users import User, UserCreate, UserUpdate
from app.utils.users_utils import get_user_by_id, get_user_by_username
from common.logger import get_logger
from common.CurrentUserContext import CurrentUserContext
from app.services.session_service import getSessionsByUserId, updateSession, deleteSession
from sqlmodel.ext.asyncio.session import AsyncSession
import redis.asyncio as redis

logger = get_logger(__name__)

async def create_user(
        session: AsyncSession,
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
    session: AsyncSession, 
    user_id: UUID
) -> User:
    
    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_fetch_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    return user

async def fetch_all_users(session: AsyncSession) -> list[User]:
    result = await session.exec(select(User))
    users = list(result.all())
    return users

async def update_user(
    redis: redis.Redis,
    session: AsyncSession, 
    user_update: UserUpdate,
    user_id: UUID
) -> User:

    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_update_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    
    if user_update.plain_password:
        hashed = get_password_hash(user_update.plain_password)
        user.hashed_password = hashed
    
    update_data = user_update.model_dump(exclude_unset=True, exclude={"plain_password"})
    for key, value in update_data.items():
        setattr(user, key, value)
    
    session.add(user)
    await session.commit()
    await session.refresh(user)

    session_ids = await getSessionsByUserId(redis, user.id)
    if not user_update.plain_password:
        for id in session_ids:
            await updateSession( redis, id, {"username": user.username})
    else:
        for id in session_ids:
            await deleteSession(redis, id)
            
    logger.info("user_updated_succesfully", user_id=user.id)
    
    return user

async def upload_avatar(
    redis: redis.Redis,
    session: AsyncSession,
    user: CurrentUserContext,
    file: UploadFile = File(...), 
):

    if file is None:
        raise NoFileException()
    
    if file.content_type is None:
        raise NoFileTypeException()
    
    if file.filename is None:
        raise NoFileNameException()

    if not file.content_type.startswith("image/"):
        raise WrongFileTypeException()

    AVATARS_DIR = FilePath("/app/static/avatars")
    AVATARS_DIR.mkdir(parents=True, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    new_filename = f"{uuid4()}.{file_extension}"
    file_path = AVATARS_DIR / new_filename

    contents = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    avatar_url = f"/static/avatars/{new_filename}"

    current_user = await get_user_by_id(session, user.user_id)
    if not current_user:
        logger.warning("user_avatar_upload_failed_not_found", user_id=user.user_id)
        raise UserNotFoundException()
    
    current_user.avatar_url = avatar_url
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    session_ids = await getSessionsByUserId(redis, current_user.id)
    for id in session_ids:
        await updateSession(redis, id, {"avatar_url": avatar_url})
        
    logger.info("user_avatar_uploaded_succesfully", user_id=user.user_id)
    return {"avatar_url": avatar_url}


async def change_user_role(    
    redis: redis.Redis,
    session: AsyncSession, 
    user_id: UUID, 
    is_superuser: bool,
):
    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_change_role_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    
    user.is_superuser = is_superuser
    session.add(user)
    await session.commit()
    await session.refresh(user)

    session_ids = await getSessionsByUserId(redis, user.id)
    for id in session_ids:
        await updateSession(redis, id, {"is_superuser": user.is_superuser})

    logger.info("user_role_changed_succesfully", user_id=user.id, new_role="admin" if is_superuser else "user")

    return {"message": "User role changed successfully", "new_role": "admin" if is_superuser else "user"}
    

async def remove_user(session: AsyncSession, user_id: UUID):
    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_remove_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    
    await session.delete(user)
    await session.commit()

    logger.info("user_removed_succesfully", user_id=user.id)

    return {"message": "User removed successfully"}