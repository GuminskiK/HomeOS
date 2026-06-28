from pydantic import BaseModel
from uuid import UUID

class SessionData(BaseModel):
    user_id: UUID
    username: str
    is_superuser: bool
    created_at: str | None
    mfa_verified: bool
    device: str
    ip: str | None