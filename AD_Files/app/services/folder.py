from AD_Files.app.models.StoragePool import FileRecord, StoragePool
from typing import List, Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from common.CurrentUserContext import CurrentUserContext
from app.schemas.files import CreateFolderRequest, FileRegisterRequest, FileItemResponse, FileRenameRequest
from sqlmodel import select

async def get_file_tree(
    session: AsyncSession,
    user: CurrentUserContext,
    parent_id: Optional[UUID] = None
):
    """Zwraca listę plików i folderów wewnątrz wskazanego folderu rodzica (lub Root, gdy parent_id jest puste)."""
    statement = select(FileRecord).where(FileRecord.parent_id == parent_id)
    results = await session.exec(statement)
    return results.all()

async def create_folder(
    folder_in: CreateFolderRequest,
    session: AsyncSession,
    user: CurrentUserContext
):
    """Tworzy czysto wirtualny folder w strukturze bazy danych."""
    new_folder = FileRecord(
        pool_id=folder_in.pool_id,           # Przypisujemy do puli (dysku)
        parent_id=folder_in.parent_id,
        filename=folder_in.name,             # ZMIANA z 'name'
        is_folder=True,
        logical_path=folder_in.logical_path  # Pełna ścieżka zamiast twardego "/"
        # size_bytes domyślnie zostanie 0
    )
    session.add(new_folder)
    await session.commit()
    await session.refresh(new_folder)
    return new_folder