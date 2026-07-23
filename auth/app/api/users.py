from typing import List
from common.CurrentUserContext import CurrentUserContext
from fastapi import APIRouter, File, UploadFile
from uuid import UUID
from app.core.user import CurrentUser, AdminUser
from app.models.Users import UserCreate, UserRead, UserUpdate
from app.services.users_service import (
    create_user,
    fetch_all_users,
    fetch_user_by_id,
    remove_user,
    update_user,
    upload_avatar,
)
from app.core.db import db_session, redis_client

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=201)
async def post_user(
    session: db_session, user: UserCreate, admin: AdminUser
):

    return await create_user(session, user)

@router.get("", response_model=List[UserRead])
async def get_all_users(session: db_session, admin: AdminUser):

    return await fetch_all_users(session)

@router.get("/me", response_model=CurrentUserContext)
async def get_current_user( current_user: CurrentUser):
    return current_user

@router.get("/{user_id}", response_model=UserRead)
async def get_user(session: db_session, user_id: UUID, admin: AdminUser):

    return await fetch_user_by_id(session, user_id)


@router.patch("/me", response_model=UserRead)
async def patch_user(
    redis: redis_client,
    session: db_session, 
    user: UserUpdate, 
    current_user: CurrentUser,
):

    user.is_superuser = False
    is_me = True

    return await update_user(redis, session, current_user, user, is_me)

@router.patch("/{user_id}", response_model=UserRead)
async def patch_user_admin(
    redis: redis_client,
    session: db_session, 
    user: UserUpdate, 
    user_id: UUID, 
    admin: AdminUser
):

    if UUID == admin.user_id:
        is_me = True

    return await update_user(redis, session, admin, user, is_me)

@router.delete("/me", response_model=UserRead)
async def delete_user(session: db_session, user: CurrentUser):

    return await remove_user(session, user.user_id)

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user_admin(
    session: db_session, user_id: UUID, admin: AdminUser
):

    return await remove_user(session, user_id)

@router.post("/me/avatar")
async def upload_avatar_route(
    redis: redis_client,
    session: db_session,
    user: CurrentUser,
    file: UploadFile = File(...), 
):
   
    avatar_url = await upload_avatar(redis, session, user, file)

    return {"avatar_url": avatar_url}