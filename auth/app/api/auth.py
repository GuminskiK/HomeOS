from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import db_session, redis_client
from app.services.auth_service import login, logout

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login_route(    
    request: Request,
    response: Response,
    redis: redis_client,
    session: db_session,
    form_data: OAuth2PasswordRequestForm = Depends(),
    mfa_code: str | None = Form(default=None),
    ):
    
    login_response = await login(
        request=request,
        response=response,
        redis=redis,
        session=session,
        form_data=form_data,
        mfa_code=mfa_code
    )
    
    return login_response

@router.post("/logout")
async def logout_route(
    request: Request, 
    response: Response, 
    redis: redis_client):

    logout_response = await logout(
        request=request, 
        response=response, 
        redis=redis
    )

    return logout_response