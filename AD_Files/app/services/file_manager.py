import os
import aiofiles
from pathlib import Path
from fastapi import HTTPException, status

class FileManager:
    @staticmethod
    def get_secure_path(mount_prefix: str, logical_path: str) -> Path:
        """
        Zabezpiecza przed atakami typu Path Traversal i zwraca bezwzględną
        fizyczną ścieżkę do pliku wewnątrz kontenera.
        """
        # Konwersja do obiektów Path i resolve() usuwa symlinki i dziwne znaki
        base_path = Path(mount_prefix).resolve()
        
        # Usuwamy ukośnik z początku logicznej ścieżki (jeśli jest), żeby nie traktowało jej jako root
        clean_logical_path = logical_path.lstrip("/")
        
        # Łączymy ścieżki
        target_path = (base_path / clean_logical_path).resolve()

        # KRYTYCZNE ZABEZPIECZENIE: Sprawdzamy czy cel faktycznie leży wewnątrz bazy
        if not str(target_path).startswith(str(base_path)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Path traversal attempt detected! Próba wyjścia poza wirtualną pulę."
            )
            
        return target_path

    @staticmethod
    async def get_file_metadata(file_path: Path) -> dict:
        """Pobiera rozmiar i podstawowe metadane pliku z dysku."""
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plik nie istnieje na dysku fizycznym."
            )
        
        file_stat = os.stat(file_path)
        return {
            "size": file_stat.st_size,
            "modified_at": file_stat.st_mtime
        }

    @staticmethod
    async def file_chunk_generator(file_path: Path, start_byte: int, end_byte: int, chunk_size: int = 1024 * 1024):
        """
        Asynchroniczny generator (yield) czytający plik w paczkach (domyślnie 1MB).
        Używa funkcji seek() aby pominąć bajty i nie zapychać RAM-u na Raspberry Pi.
        """
        bytes_to_read = end_byte - start_byte + 1
        
        async with aiofiles.open(file_path, mode="rb") as f:
            # Przeskakujemy na dysku fizycznym prosto do żądanego miejsca
            await f.seek(start_byte)
            
            bytes_remaining = bytes_to_read
            
            while bytes_remaining > 0:
                # Zabezpieczenie przed pobraniem za dużego chunka na samym końcu
                current_chunk_size = min(chunk_size, bytes_remaining)
                chunk = await f.read(current_chunk_size)
                
                if not chunk:
                    break
                    
                bytes_remaining -= len(chunk)
                yield chunk