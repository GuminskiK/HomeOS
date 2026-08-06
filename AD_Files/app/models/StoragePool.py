import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from .FileRecord import FileRecord
# --- PULA PAMIĘCI (STORAGE POOL) ---

class StoragePoolBase(SQLModel):
    name: str = Field(index=True, max_length=100, description="Przyjazna nazwa, np. 'Główny dysk NVMe'")
    mount_prefix: str = Field(
        max_length=255, 
        unique=True, 
        description="Fizyczna ścieżka montowania wewnątrz kontenera, np. '/app/storage/nvme1'"
    )
    is_active: bool = Field(default=True)

class StoragePool(StoragePoolBase, table=True):
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relacja do plików
    files: List["FileRecord"] = Relationship(back_populates="pool")
