from uuid import UUID
from fastapi import File, Form, Request, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from AD_Files.app.models.StoragePool import StoragePool
from AD_Files.app.services.file_manager import FileManager
from common.CurrentUserContext import CurrentUserContext
from AD_Files.app.schemas.files import FileRegisterRequest
import re
from app.core.exceptions import (
    InvalidFilePathException, InvalidStoragePoolIdException, FileNotFoundException, InvalidRangeHeaderException,
    FailedToSaveFileException, RequestedRangeNotSatisfiableException
)
from typing import Optional
from app.models.FileRecord import FileRecord
import aiofiles

async def register_external_file(
    session: AsyncSession,
    user: CurrentUserContext,
    payload: FileRegisterRequest,
):
    """
    KRYTYCZNE DLA AGREGATORA:
    Wewnętrzny endpoint rejestrujący plik na dysku pobrany np. przez yt-dlp w kontenerze homeos-aggregator.
    """
    pool = await session.get(StoragePool, payload.pool_id)
    if not pool or not pool.is_active:
        raise InvalidStoragePoolIdException()

    # Obliczenie fizycznej ścieżki i weryfikacja czy plik fizycznie istnieje na dysku
    target_path = FileManager.get_secure_path(pool.mount_prefix, payload.logical_path)
    metadata = await FileManager.get_file_metadata(target_path)

    new_file = FileRecord(
        pool_id=payload.pool_id,
        parent_id=payload.parent_id,
        filename=payload.filename,           # ZMIANA z 'name'
        is_folder=False,
        size_bytes=metadata["size"],         # ZMIANA z 'size'
        mime_type=payload.mime_type,
        logical_path=payload.logical_path
    )
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file


async def stream_file(
    file_id: UUID,
    request: Request,
    session: AsyncSession,
):
    """
    Zwraca strumień bajtów pliku. Obsługuje nagłówek Range, co pozwala 
    odtwarzaczom wideo na przewijanie i porcjowanie danych.
    """
    # 1. Pobierz logiczny rekord pliku z bazy danych
    file_record = await session.get(FileRecord, file_id)
    if not file_record or file_record.is_folder:
        raise FileNotFoundException()

    # 2. Pobierz przypisaną wirtualną pulę pamięci
    pool = await session.get(StoragePool, file_record.pool_id)
    if not pool or not pool.is_active:
        raise InvalidStoragePoolIdException()

    # 3. Wylicz bezpieczną ścieżkę na dysku fizycznym
    file_path = FileManager.get_secure_path(pool.mount_prefix, file_record.logical_path)
    
    # 4. Pobierz fizyczne parametry pliku z dysku
    metadata = await FileManager.get_file_metadata(file_path)
    file_size = metadata["size"]

    # 5. Magia odtwarzacza wideo: Obsługa nagłówka Range
    range_header = request.headers.get("Range")
    
    if not range_header:
        # Żądanie całego pliku na raz (HTTP 200 OK)
        headers = {
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes"
        }
        return StreamingResponse(
            FileManager.file_chunk_generator(file_path, 0, file_size - 1),
            media_type=file_record.mime_type or "application/octet-stream",
            headers=headers
        )

    # Parsowanie nagłówka Range (przeglądarka prosi np. o "bytes=3276800-6553600")
    range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
    if not range_match:
        raise InvalidRangeHeaderException()

    start_byte = int(range_match.group(1))
    # Jeśli przeglądarka nie podała końca (np. "bytes=100-"), wysyłamy do samego końca pliku
    end_byte = int(range_match.group(2)) if range_match.group(2) else file_size - 1

    # Zabezpieczenie przed prośbą o bajty z kosmosu
    if start_byte >= file_size or end_byte >= file_size:
        raise RequestedRangeNotSatisfiableException()

    chunk_length = end_byte - start_byte + 1

    headers = {
        "Content-Range": f"bytes {start_byte}-{end_byte}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_length),
    }

    # Zwracamy HTTP 206 Partial Content - odtwarzacz wie, że dostał tylko kawałek!
    return StreamingResponse(
        FileManager.file_chunk_generator(file_path, start_byte, end_byte),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type=file_record.mime_type or "application/octet-stream",
        headers=headers
    )

async def upload_file_stream(

    session: AsyncSession,
    user: CurrentUserContext,
    pool_id: UUID = Form(...),
    parent_id: Optional[UUID] = Form(None),
    logical_dir: str = Form(...), # np. "documents" - folder docelowy w logice bazy
    file: UploadFile = File(...),
):
    """
    Strumieniowy zapis pliku z ominięciem buforowania w RAM.
    Bezpieczny nawet dla nieco większych plików na Raspberry Pi.
    """
    # 1. Weryfikacja puli
    pool = await session.get(StoragePool, pool_id)
    if not pool or not pool.is_active:
        raise InvalidStoragePoolIdException()

    # 2. Zabezpieczenie logicznej ścieżki (złączamy folder + nazwa pliku)
    if file.filename is None or file.filename.strip() == "":
        raise InvalidFilePathException()

    safe_filename = file.filename.replace("/", "") # Proste zabezpieczenie nazwy
    logical_path = f"{logical_dir.strip('/')}/{safe_filename}"
    
    # Wyliczamy fizyczną ścieżkę na dysku
    target_path = FileManager.get_secure_path(pool.mount_prefix, logical_path)

    # Upewniamy się, że fizyczny folder nadrzędny istnieje
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 3. Zapis strumieniowy bezpośrednio na dysk (chunk po chunku)
    try:
        async with aiofiles.open(target_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # Czytamy po 1MB
                await buffer.write(chunk)
    except Exception as e:
        raise FailedToSaveFileException()
    finally:
        await file.close()

    # 4. Zapis do bazy danych
    metadata = await FileManager.get_file_metadata(target_path)
    
    new_file = FileRecord(
        pool_id=pool_id,
        parent_id=parent_id,
        filename=safe_filename,              # ZMIANA z 'name'
        is_folder=False,
        size_bytes=metadata["size"],         # ZMIANA z 'size'
        mime_type=file.content_type,
        logical_path=logical_path
    )
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    
    return new_file

async def download_file(
    session: AsyncSession,
    user: CurrentUserContext,
    file_id: UUID,
):
    """Wymusza pobranie pliku jako załącznika (zamiast otwierania/streamowania w przeglądarce)."""
    file_record = await session.get(FileRecord, file_id)
    if not file_record or file_record.is_folder:
        raise FileNotFoundException()

    pool = await session.get(StoragePool, file_record.pool_id)
    if not pool or not pool.is_active:
        raise InvalidStoragePoolIdException()

    file_path = FileManager.get_secure_path(pool.mount_prefix, file_record.logical_path)
    
    if not file_path.exists():
        raise FileNotFoundException()

    return FileResponse(
        path=file_path,
        filename=file_record.filename,  # ZMIANA: używamy .filename
        media_type=file_record.mime_type or "application/octet-stream",
        # ZMIANA: używamy .filename w nagłówku
        headers={"Content-Disposition": f'attachment; filename="{file_record.filename}"'}
    )