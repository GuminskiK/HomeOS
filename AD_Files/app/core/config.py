from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".../.env", env_file_encoding="utf-8")

    # Application settings
    APP_NAME: str = "HomeOS Files"
    SECRET_KEY: str = "your-super-secret-key-change-this"
    DUMMY_HASH: str = "$argon2id$v=19$m=65536,t=2,p=2$Wm9uZQ$Wm9uZQ"

    # Database settings
    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Session settings
    SESSION_SECRET_KEY: str = "your-super-strategic-secret-key-change-this"
    SESSION_TTL: int = 48 * 3600
    SESSION_COOKIE_NAME: str = "homeos_session"
    SESSION_SAME_SITE: Literal['lax', 'strict', 'none'] = "lax"
    SESSION_HTTP_ONLY: bool = True
    SESSION_SECURE: bool = False

settings = Settings()