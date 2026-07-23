from contextlib import asynccontextmanager
import json
from fastapi.staticfiles import StaticFiles
from sqlmodel import select
from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from common.rate_limiting import limiter, custom_rate_limit_handler
from common.logger import setup_logging
from common.logging_middleware import StructlogMiddleware
from app.core.config import settings
from app.models.Users import User

import os
import shutil

from app.api import auth, apikeys, two_fa, users

setup_logging(json_logs=False, log_level="INFO")

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    from app.core.db import db_deps

    AsyncSessionLocal = db_deps.AsyncSessionLocal()

    async with AsyncSessionLocal as session:
        query = select(User).where(User.api_keys != None)
        result = await session.exec(query)
        users = result.all()
        for user in users:
            for api_key in user.api_keys:
                await db_deps.get_redis().set(f"apikey:{api_key.hashed_key}", json.dumps({"id": api_key.user_id, "username": user.username, "is_superuser": user.is_superuser}))
    
    print("Zsynchronizowano klucze API z Redis")

    async with AsyncSessionLocal as session:
        query = select(User)
        result = await session.exec(query)
        users = result.all()
    
        if not users:
            from app.utils.auth_utils import get_password_hash

            hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                hashed_password=hashed_password,
                is_superuser=True,
            )
            session.add(admin_user)
            await session.commit()
            print("Utworzono domyślnego użytkownika administratora")
    
    yield

app = FastAPI(lifespan=lifespan, title=settings.APP_NAME, root_path="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("static/avatars", exist_ok=True)

app.add_middleware(StructlogMiddleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth.router)
app.include_router(two_fa.router)
app.include_router(apikeys.router)
app.include_router(users.router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}