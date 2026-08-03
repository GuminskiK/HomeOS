from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.user import AdminUser
from app.services.docker_manager import docker_manager

router = APIRouter(prefix="/containers", tags=["Container Management"])

class ContainerAction(BaseModel):
    action: str

@router.get("/")
async def get_containers_list(user: AdminUser):
    """Zwraca listę wszystkich mikroserwisów HomeOS i ich status."""

    return await docker_manager.list_homeos_containers()


@router.post("/{container_name}/control")
async def control_container(container_name: str, payload: ContainerAction, user: AdminUser):
    """Uruchamia, zatrzymuje lub restartuje kontener."""

    return await docker_manager.control_container(container_name, payload.action)


@router.get("/{container_name}/logs")
async def get_logs(container_name: str, user: AdminUser, tail: int = 50):
    """Pobiera ostatnie logi z wybranego kontenera."""

    return await docker_manager.get_container_logs(container_name, tail)

@router.get("/{container_name}/stats")
async def get_container_stats(container_name: str, user: AdminUser):
    """Pobiera aktualne statystyki użycia zasobów dla danego kontenera."""
        
    return await docker_manager.get_container_stats(container_name)
