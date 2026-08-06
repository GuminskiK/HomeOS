from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.core.db import db_session
from app.core.user import CurrentUser, AdminUser

from AD_Files.app.models.StoragePool import StoragePool
from app.schemas.files import StoragePoolCreate, StoragePoolRead

from app.services.pools import create_pool, list_pools

router = APIRouter(prefix="/pools", tags=["storage-pools"])

@router.get("", response_model=List[StoragePoolRead])
async def list_pools_route(
    session: db_session,
    user: CurrentUser
):
    """Zwraca listę wszystkich aktywnych pul pamięci."""

    return await list_pools(session=session, user=user)

@router.post("", response_model=StoragePoolRead, status_code=status.HTTP_201_CREATED)
async def create_pool_route(
    pool_in: StoragePoolCreate,
    session: db_session,
    user: CurrentUser,
    admin: AdminUser
):
    """Rejestruje nową pulę pamięci masowej (wymagane uprawnienia administratora)."""

    return await create_pool(pool_in=pool_in, session=session, user=user)