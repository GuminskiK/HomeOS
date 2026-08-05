import aiodocker
from typing import List, Dict, Any

from common.logger import get_logger
from app.core.exceptions import (
    ContainerNotFoundException, FailedToExecuteActionOnContainerException, FailedToGetContainersStatsException, ForbiddenFromManagingThisContainerException, InvalidContainerActionException
)

logger = get_logger(__name__)
valid_actions = ["start", "stop", "restart"]

class DockerManager:
    def __init__(self):
        self.allowed_prefix = "homeos-"

    async def list_homeos_containers(self) -> List[Dict[str, Any]]:
        async with aiodocker.Docker() as docker:
            containers = await docker.containers.list(all=True)
            
            result = []
            for container in containers:
                name = container._container["Names"][0].lstrip("/")
                
                if name.startswith(self.allowed_prefix):
                    state = container._container["State"]
                    result.append({
                        "id": container._id,
                        "name": name,
                        "state": state,
                        "status": container._container["Status"],
                        "image": container._container["Image"]
                    })
            logger.info(f"Znaleziono {len(result)} kontenerów z prefiksem '{self.allowed_prefix}'")
            return result

    async def control_container(self, container_name: str, action: str) -> bool:
        """action może być 'start', 'stop', lub 'restart'"""
        if action not in valid_actions:
            raise InvalidContainerActionException()
        if not container_name.startswith(self.allowed_prefix):
            logger.warning(f"Nieautoryzowana próba zarządzania kontenerem: {container_name}")
            raise ForbiddenFromManagingThisContainerException()
        
        async with aiodocker.Docker() as docker:
            try:
                container = await docker.containers.get(container_name)
                
                if action == "start":
                    await container.start()
                    logger.info(f"Kontener '{container_name}' został uruchomiony.")
                elif action == "stop":
                    await container.stop()
                    logger.info(f"Kontener '{container_name}' został zatrzymany.")
                elif action == "restart":
                    await container.restart()
                    logger.info(f"Kontener '{container_name}' został zrestartowany.")
                else:
                    return False
                return True
            except aiodocker.exceptions.DockerError:
                logger.error(f"Nie udało się wykonać akcji '{action}' na kontenerze '{container_name}'.")
                raise FailedToExecuteActionOnContainerException()

    async def get_container_logs(self, container_name: str, tail: int = 100) -> List[str]:
        if not container_name.startswith(self.allowed_prefix):
            logger.warning(f"Nieautoryzowana próba pobrania logów kontenera: {container_name}")
            raise ForbiddenFromManagingThisContainerException()

        async with aiodocker.Docker() as docker:
            try:
                container = await docker.containers.get(container_name)
                logs = await container.log(stdout=True, stderr=True, tail=tail)
                logger.info(f"Pobrano {len(logs)} logów dla kontenera '{container_name}'.")
                return logs
            except aiodocker.exceptions.DockerError as e:

                if e.status == 404:
                    logger.error(f"Kontener '{container_name}' nie istnieje.")
                    raise ContainerNotFoundException(resource_name=container_name)
                else:
                    logger.error(f"Błąd podczas pobierania logów dla kontenera '{container_name}': {e}")
                    raise FailedToExecuteActionOnContainerException()

    async def get_container_stats(self, container_name: str) -> dict:
        if not container_name.startswith(self.allowed_prefix):
            logger.warning(f"Nieautoryzowana próba pobrania statystyk kontenera: {container_name}")
            raise ForbiddenFromManagingThisContainerException()

        async with aiodocker.Docker() as docker:
            try:
                container = await docker.containers.get(container_name)
                
                # stream=False sprawia, że pobieramy jedną, aktualną "klatkę" danych (snapshot)
                stats = await container.stats(stream=False)
                
                # aiodocker zwraca czasem listę jednoelementową, rozpakowujemy ją
                stats_data = stats[0] if isinstance(stats, list) else stats

                # === Obliczanie Pamięci RAM ===
                mem_usage = stats_data.get("memory_stats", {}).get("usage", 0)
                mem_limit = stats_data.get("memory_stats", {}).get("limit", 0)
                
                mem_usage_mb = round(mem_usage / (1024 * 1024), 2)
                mem_limit_mb = round(mem_limit / (1024 * 1024), 2)
                mem_percent = round((mem_usage / mem_limit) * 100, 2) if mem_limit > 0 else 0.0

                # === Obliczanie Użycia CPU ===
                # Docker wylicza % CPU na podstawie różnicy między obecnym a poprzednim pomiarem
                cpu_delta = stats_data.get("cpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0) - \
                            stats_data.get("precpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0)
                
                system_delta = stats_data.get("cpu_stats", {}).get("system_cpu_usage", 0) - \
                               stats_data.get("precpu_stats", {}).get("system_cpu_usage", 0)
                
                cpu_percent = 0.0
                if system_delta > 0 and cpu_delta > 0:
                    percpu_usage = stats_data.get("cpu_stats", {}).get("cpu_usage", {}).get("percpu_usage", [])
                    # Ilość rdzeni przydzielona do kontenera
                    online_cpus = len(percpu_usage) if percpu_usage else 1
                    cpu_percent = round((cpu_delta / system_delta) * online_cpus * 100.0, 2)

                logger.info(f"Pobrano statystyki dla kontenera '{container_name}': "
                            f"CPU: {cpu_percent}%, RAM: {mem_usage_mb}/{mem_limit_mb} MB ({mem_percent}%)")

                return {
                    "memory_usage_mb": mem_usage_mb,
                    "memory_limit_mb": mem_limit_mb,
                    "memory_percent": mem_percent,
                    "cpu_percent": cpu_percent
                }

            except aiodocker.exceptions.DockerError as e:

                if e.status == 404:
                    logger.error(f"Kontener '{container_name}' nie istnieje.")
                    raise ContainerNotFoundException(resource_name=container_name)
                else:
                    logger.error(f"Błąd podczas pobierania statystyk dla kontenera '{container_name}': {e}")
                    raise FailedToGetContainersStatsException()

docker_manager = DockerManager()