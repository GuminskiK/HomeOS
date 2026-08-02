from common.users import AuthDependency, CurrentUserContext
from app.core.config import settings
from app.core.db import redis_pure, db_deps
from app.models.Users import User
from fastapi import Depends
from typing import Annotated
from common.users import CurrentUserContext

session = db_deps.AsyncSessionLocal()

auth_dependency = AuthDependency(
    session_cookie_name=settings.SESSION_COOKIE_NAME,
    session_ttl=settings.SESSION_TTL,
    redis=redis_pure,
    db_session=session
)

CurrentUser = Annotated[CurrentUserContext, Depends(auth_dependency.get_current_session)]
AdminUser = Annotated[CurrentUserContext, Depends(auth_dependency.get_current_admin_session())]