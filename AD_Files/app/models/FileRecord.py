import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from AD_Files.app.models.StoragePool import StoragePool

class FileRecordBase(SQLModel):
    # Pula pamięci (każdy plik i folder musi wiedzieć, na jakim dysku fizycznie leży)
    pool_id: uuid.UUID = Field(foreign_key="files_storage_pools.id")
    
    # KLUCZOWE: Brakowało tego pola! Relacja do nadrzędnego folderu
    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="files_records.id")
    
    logical_path: str = Field(index=True, max_length=1024)
    
    # Używamy konsekwentnie 'filename' (zamiast 'name')
    filename: str = Field(index=True, max_length=255) 
    
    is_folder: bool = Field(default=False)
    
    mime_type: Optional[str] = Field(default=None, description="np. 'video/mp4'")
    
    # Używamy konsekwentnie 'size_bytes' (zamiast 'size')
    size_bytes: int = Field(default=0)

class FileRecord(FileRecordBase, table=True):
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    pool: StoragePool = Relationship(back_populates="files")