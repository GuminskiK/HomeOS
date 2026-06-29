from fastapi import APIRouter

from app.core.user import current_user, admin_or_owner_user
from app.services.apikeys_service import (
    fetch_user_apikeys,
    generate_api_key_for_user,
    revoke_user_api_key
)
from app.core.db import db_session, redis_client

router = APIRouter(prefix="/apikeys", tags=["apikeys"])

@router.post("", status_code=201)
async def post_apikey(user: current_user, session: db_session, name: str, redis: redis_client):

    return await generate_api_key_for_user(session, user.id, name, redis)


@router.delete("/{key_id}")
async def delete_api_key(key_id: int, user: admin_or_owner_user, session: db_session, redis: redis_client):

    return await revoke_user_api_key(session, user.id, key_id, redis)


@router.get("")
async def get_my_keys(user: admin_or_owner_user, session: db_session):
    return await fetch_user_apikeys(user, session)