
from uuid import UUID
from fastapi import APIRouter, Form,  Request, status, File, UploadFile
from app.core.db import db_session
from typing import List, Optional
from app.schemas.files import CreateFolderRequest, FileRegisterRequest, FileItemResponse, FileRenameRequest
from app.core.user import CurrentUser

from app.services.folder import get_file_tree, create_folder
from app.services.stream import register_external_file, stream_file, upload_file_stream, download_file
from app.services.files import delete_file, rename_file

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/tree", response_model=List[FileItemResponse])
async def get_file_tree_route(
    session: db_session,
    user: CurrentUser,
    parent_id: Optional[UUID] = None,
    
):
    """Zwraca listę plików i folderów wewnątrz wskazanego folderu rodzica (lub Root, gdy parent_id jest puste)."""

    return await get_file_tree(parent_id=parent_id, session=session, user=user)

@router.post("/folder", response_model=FileItemResponse, status_code=status.HTTP_201_CREATED)
async def create_folder_route(
    folder_in: CreateFolderRequest,
    session: db_session,
    user: CurrentUser
):
    """Tworzy czysto wirtualny folder w strukturze bazy danych."""

    return await create_folder(folder_in=folder_in, session=session, user=user)

@router.post("/register", response_model=FileItemResponse, status_code=status.HTTP_201_CREATED)
async def register_external_file_route(
    payload: FileRegisterRequest,
    session: db_session,
    user: CurrentUser
):
    """
    KRYTYCZNE DLA AGREGATORA:
    Wewnętrzny endpoint rejestrujący plik na dysku pobrany np. przez yt-dlp w kontenerze homeos-aggregator.
    """
    return await register_external_file(session=session, user=user, payload=payload)


@router.get("/stream/{file_id}")
async def stream_file_route(
    file_id: UUID,
    request: Request,
    session: db_session,
    user: CurrentUser  # KRYTYCZNE: Endpoint chroniony sesją!
):
    """
    Zwraca strumień bajtów pliku. Obsługuje nagłówek Range, co pozwala 
    odtwarzaczom wideo na przewijanie i porcjowanie danych.
    """
    return await stream_file(file_id=file_id, request=request, session=session)

@router.post("/upload", response_model=FileItemResponse, status_code=status.HTTP_201_CREATED)
async def upload_file_stream(
    session: db_session,
    user: CurrentUser,
    pool_id: UUID = Form(...),
    parent_id: Optional[UUID] = Form(None),
    logical_dir: str = Form(...), # np. "documents" - folder docelowy w logice bazy
    file: UploadFile = File(...),
    
):
    """
    Strumieniowy zapis pliku z ominięciem buforowania w RAM.
    Bezpieczny nawet dla nieco większych plików na Raspberry Pi.
    """

    return upload_file_stream(session=session, user=user, pool_id=pool_id, parent_id=parent_id, logical_dir=logical_dir, file=file)

@router.get("/download/{file_id}")
async def download_file(
    session: db_session,
    user: CurrentUser,
    file_id: UUID,
):
    """Wymusza pobranie pliku jako załącznika (zamiast otwierania/streamowania w przeglądarce)."""

    return await download_file(session=session, user=user, file_id=file_id)



@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_route(
    session: db_session,
    user: CurrentUser,
    file_id: UUID,
):
    """Usuwa plik/folder z bazy danych ORAZ fizycznie z dysku."""

    return await delete_file(file_id=file_id, session=session, user=user)

@router.patch("/{file_id}", response_model=FileItemResponse)
async def rename_file_route(
    session: db_session,
    user: CurrentUser,
    file_id: UUID,
    payload: FileRenameRequest,
):
    """Zmienia nazwę pliku w bazie oraz na dysku fizycznym."""
    
    return await rename_file(file_id=file_id, payload=payload, session=session, user=user)