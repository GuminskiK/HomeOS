import json
from sqlmodel import SQLModel
from fastapi import Depends, HTTPException, status, Request, Response
from common.exceptions import (
    AdminNeededException, AdminOrOwnerNeededException
)
from common.SessionData import SessionData
import redis.asyncio as redis
class CurrentUserContext(SQLModel):
    id: int
    username: str
    is_superuser: bool


class AuthDependency:
    def __init__(self, session_cookie_name: str, session_ttl: int, redis: redis.Redis):
        self.session_cookie_name = session_cookie_name
        self.SESSION_TTL = session_ttl
        self.redis = redis


    async def get_current_session(self, request: Request, response: Response) -> SessionData:
        session_id = request.cookies.get(self.session_cookie_name)
        if not session_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Brak sesji")
        
        redis_key = f"session:{session_id}"
        session_raw = await self.redis.get(redis_key)
        
        if not session_raw:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesja wygasła lub nie istnieje")
        
        session_data = SessionData(**json.loads(session_raw))
        
        await self.redis.expire(redis_key, self.SESSION_TTL)
        
        response.set_cookie(
            key=self.session_cookie_name,
            value=session_id,
            max_age=self.SESSION_TTL,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        
        return session_data

    def get_current_admin_session(self):
        async def _get_current_admin_user(
            current_user: CurrentUserContext = Depends(self.get_current_session)
        ) -> CurrentUserContext:
            if not current_user.is_superuser:
                raise AdminNeededException()
            return current_user
        return _get_current_admin_user

    def get_current_owner_or_admin_session(self):
        async def _get_current_owner_or_admin_user(
            user_id: int,
            current_user: CurrentUserContext = Depends(self.get_current_session)
        ) -> CurrentUserContext:
            if current_user.id != user_id and not current_user.is_superuser:
                raise AdminOrOwnerNeededException()
            return current_user
        return _get_current_owner_or_admin_user
