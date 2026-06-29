from typing import List

from fastapi import APIRouter
from uuid import UUID
from app.core.user import current_user, admin_user
from app.models.Users import UserCreate, UserRead, UserUpdate
from app.services.users_service import (
    create_user,
    fetch_all_users,
    fetch_user_by_id,
    remove_user,
    update_user,
)
from app.core.db import db_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=201)
async def post_user(
    session: db_session, user: UserCreate, admin: admin_user
):

    return await create_user(session, user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(session: db_session, user_id: UUID, admin: admin_user):

    return await fetch_user_by_id(session, user_id)


@router.get("", response_model=List[UserRead])
async def get_all_users(session: db_session, admin: admin_user):

    return await fetch_all_users(session)


@router.patch("/{user_id}", response_model=UserRead)
async def patch_user_admin(
    session: db_session, 
    user: UserUpdate, 
    user_id: UUID, 
    admin: admin_user
):

    return await update_user(session, user_id, user)


@router.patch("/me", response_model=UserRead)
async def patch_user(
    session: db_session, user: UserUpdate, current_user: current_user
):

    user.is_superuser = False

    return await update_user(session, current_user.id, user)


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user_admin(
    session: db_session, user_id: UUID, admin: admin_user
):

    return await remove_user(session, user_id)


@router.delete("/me", response_model=UserRead)
async def delete_user(session: db_session, user: current_user):

    return await remove_user(session, user.id)
