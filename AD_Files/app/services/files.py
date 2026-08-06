from AD_Files.app.schemas.files import FileRenameRequest
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from AD_Files.app.models.StoragePool import StoragePool
from AD_Files.app.services.file_manager import FileManager
from common.CurrentUserContext import CurrentUserContext
from app.models.FileRecord import FileRecord
import os
import shutil
from app.core.exceptions import (
    InvalidStoragePoolIdException, FileNotFoundException, InvalidRangeHeaderException)


async def delete_file(
    session: AsyncSession,
    user: CurrentUserContext,
    file_id: UUID,
):
    file_record = await session.get(FileRecord, file_id)
    if not file_record:
        raise FileNotFoundException()

    pool = await session.get(StoragePool, file_record.pool_id)
    
    # 1. Usuwanie fizyczne z dysku (tylko jeśli pula jest aktywna i wiemy, gdzie to leży)
    if pool and pool.is_active:
        try:
            file_path = FileManager.get_secure_path(pool.mount_prefix, file_record.logical_path)
            if file_path.exists():
                if file_record.is_folder:
                    # Usuwa folder wraz z zawartością - ostrożnie!
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
        except Exception as e:
            # Nie przerywamy, jeśli plik fizycznie nie istniał (zależy nam na wyczyszczeniu bazy)
            print(f"Błąd podczas usuwania fizycznego: {e}")

    # 2. Jeśli to folder, to trzeba rekursywnie usunąć dzieci z bazy
    # (W uproszczeniu: najlepiej tu użyć CASCADE w bazie lub osobnego skryptu, 
    # dla bezpieczeństwa usuwamy ten konkretny węzeł).
    await session.delete(file_record)
    await session.commit()
    
    return None

async def rename_file(
    session: AsyncSession,
    user: CurrentUserContext,
    file_id: UUID,
    payload: FileRenameRequest
):
    file_record = await session.get(FileRecord, file_id)
    if not file_record:
        raise FileNotFoundException()

    pool = await session.get(StoragePool, file_record.pool_id)
    if not pool or not pool.is_active:
        raise InvalidStoragePoolIdException()

    old_path = FileManager.get_secure_path(pool.mount_prefix, file_record.logical_path)
    
    # Obliczenie nowej ścieżki logicznej i fizycznej
    # (Zastępujemy stary filename nowym na końcu ścieżki)
    logical_dir = "/".join(file_record.logical_path.rstrip("/").split("/")[:-1])
    safe_new_name = payload.new_name.replace("/", "")
    new_logical_path = f"{logical_dir}/{safe_new_name}" if logical_dir else safe_new_name
    
    new_path = FileManager.get_secure_path(pool.mount_prefix, new_logical_path)

    # Fizyczna zmiana nazwy
    if old_path.exists():
        os.rename(old_path, new_path)
    
    # Aktualizacja w bazie
    file_record.name = safe_new_name
    file_record.logical_path = new_logical_path
    
    session.add(file_record)
    await session.commit()
    await session.refresh(file_record)
    
    return file_record