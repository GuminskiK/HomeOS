import base64
import io

import pyotp
import qrcode

from app.core.config import settings
from app.core.exceptions import (
    Invalid2FACodeException,
    TwoFaAlreadyEnabledException,
    TwoFaNotEnabledException,
    TwoFaNotInitiatedException,
    TwoFaSecretMissingException,
)
from app.models.Users import User
from app.core.db import db_session
from common.logger import get_logger

logger = get_logger(__name__)


async def generate_setup_data(user: User, session: db_session):
    if user.is_totp_enabled:
        logger.info("2fa_setup_already_enabled", user_id=str(user.id))
        raise TwoFaAlreadyEnabledException()

    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user.username, issuer_name=settings.APP_NAME
    )

    qr = qrcode.make(provisioning_uri)
    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr)
    qr_b64 = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

    logger.info("2fa_setup_data_generated", user_id=str(user.id))
    return {
        "secret": secret,
        "qr_code_base64": f"data:image/png;base64,{qr_b64}",
    }


async def verify_and_enable(user: User, session: db_session, code: str):

    if user.is_totp_enabled:
        raise TwoFaAlreadyEnabledException()

    if not user.totp_secret:
        raise TwoFaNotInitiatedException()

    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(code):
        raise Invalid2FACodeException()

    user.is_totp_enabled = True
    session.add(user)
    await session.commit()

    logger.info("2fa_enabled", user_id=str(user.id))

    return {"message": "2FA successfully enabled"}


async def verify_and_disable(user: User, session: db_session, code: str):

    if not user.is_totp_enabled:
        raise TwoFaNotEnabledException()

    if not user.totp_secret:
        raise TwoFaSecretMissingException()

    totp = pyotp.TOTP(user.totp_secret)

    if not totp.verify(code):
        raise Invalid2FACodeException()

    user.is_totp_enabled = False
    user.totp_secret = None
    session.add(user)
    await session.commit()

    logger.info("2fa_disabled", user_id=str(user.id))

    return {"message": "2FA successfully disabled"}
