import shutil

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
from app.core.db import db_session, redis_client
from common.logger import get_logger
from common.CurrentUserContext import CurrentUserContext
from app.services.session_service import getSessionsByUserId, updateSession

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
    redis: redis_client,
    session: db_session, 
    current_user: CurrentUserContext, 
    user_update: UserUpdate,
    is_me: bool
) -> User:

    user = await get_user_by_id(session, current_user.user_id)
    if not user:
        logger.warning("user_update_failed_not_found", user_id=current_user.user_id)
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

    session_id = await getSessionsByUserId(redis, current_user.user_id)
    await updateSession( redis, session_id[0], {"username": user.username, "is_superuser": user.is_superuser, "is_totp_enabled": user.is_totp_enabled, "avatar_url": user.avatar_url})
    logger.info("user_updated_succesfully", user_id=current_user.user_id)
    
    return user

async def upload_avatar(
    redis: redis_client,
    session: db_session,
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

    file_extension = file.filename.split(".")[-1]
    new_filename = f"{uuid4()}.{file_extension}"
    file_path = f"static/avatars/{new_filename}"

    # 3. Zapis pliku na dysku
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Wygenerowanie URL (zależnie od Twojej domeny)
    avatar_url = f"/static/avatars/{new_filename}"

    # 5. Aktualizacja w bazie danych
    current_user = await get_user_by_id(session, user.user_id)
    if not current_user:
        logger.warning("user_avatar_upload_failed_not_found", user_id=user.user_id)
        raise UserNotFoundException()
    
    current_user.avatar_url = avatar_url
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)

    await updateSession(redis, user.session_id, {"avatar_url": avatar_url})
    logger.info("user_avatar_uploaded_succesfully", user_id=user.user_id)
    return {"avatar_url": avatar_url}

async def remove_user(session: db_session, user_id: UUID):
    user = await get_user_by_id(session, user_id)
    if not user:
        logger.warning("user_remove_failed_not_found", user_id=user_id)
        raise UserNotFoundException()
    
    await session.delete(user)
    await session.commit()

    logger.info("user_removed_succesfully", user_id=user.id)

    return {"message": "User removed successfully"}