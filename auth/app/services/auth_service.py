from fastapi import Depends, Form, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from common.SessionData import SessionData
from app.core.db import db_session, redis_client
from app.utils.auth_utils import verify_password
from app.utils.users_utils import get_user_by_username
from app.core.exceptions import (
    InvalidCredentialsException,
    Required2FACodeException,
    Invalid2FACodeException,
    TwoFaSecretMissingException
)
import asyncio
import uuid
import pyotp
from datetime import timezone, datetime
from app.core.config import settings
from common.logger import get_logger
from app.services.session_service import createSession
logger = get_logger(__name__)

async def login(
    request: Request,
    response: Response,
    redis: redis_client,
    session: db_session,
    form_data: OAuth2PasswordRequestForm = Depends(),
    mfa_code: str | None = Form(default=None),
):

    await asyncio.sleep(1)

    user = await get_user_by_username(session, form_data.username)
    if not user:
        verify_password(form_data.password, settings.DUMMY_HASH)
        logger.warning("invalid_user_login_attempt", username=form_data.username)
        raise InvalidCredentialsException()

    if not verify_password(form_data.password, user.hashed_password):
        logger.warning("invalid_credentials_attempt", username=form_data.username)
        raise InvalidCredentialsException()


    if user.is_totp_enabled:
        if not mfa_code:
            logger.info("2fa_code_missing", username=user.username)
            raise Required2FACodeException()

        if user.totp_secret is None:
            raise TwoFaSecretMissingException()
        
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(mfa_code):
            logger.warning("invalid_2fa_code_attempt", username=user.username)
            raise Invalid2FACodeException()

    await createSession(request, response, user, redis)

    logger.info("user_logged_in", user_id=str(user.id), uuid=str(user.id))

    return {"message": "Logged in successfully!"}

async def logout(request: Request, response: Response, redis: redis_client):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if session_id:
        await redis.delete(f"session:{session_id}")
    response.delete_cookie(settings.SESSION_COOKIE_NAME)

    logger.info("user_logged_out", session_id=str(session_id))

    return {"message": "Wylogowano pomyślnie, sesja zniszczona"}