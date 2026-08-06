from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# --- WIRTUALNE PULE PAMĘCI ---
class StoragePoolCreate(BaseModel):
    name: str                  # np. "Dysk Główny NVMe", "NAS Synology"
    mount_prefix: str          # np. "/app/storage/nvme1"
    description: Optional[str] = None

class StoragePoolRead(StoragePoolCreate):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- STRUKTURA KATALOGÓW I PLIKÓW ---
class CreateFolderRequest(BaseModel):
    name: str
    pool_id: UUID                     # DODANE: Wskazujemy dysk/pulę dla folderu
    parent_id: Optional[UUID] = None  # None = root
    logical_path: str                 # np. "movies/action" (żebyśmy znali pełną ścieżkę)

class FileRegisterRequest(BaseModel):
    """Żądanie rejestracji pliku zapisanego na dysku np. przez mikroserwis Aggregator"""
    pool_id: UUID
    logical_path: str                 # np. "/media/youtube/film_123.mp4"
    filename: str
    mime_type: Optional[str] = "video/mp4"
    parent_id: Optional[UUID] = None

class FileItemResponse(BaseModel):
    id: UUID
    name: str
    is_folder: bool
    mime_type: Optional[str] = None
    size: Optional[int] = None
    parent_id: Optional[UUID] = None
    pool_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FileRenameRequest(BaseModel):
    new_name: str