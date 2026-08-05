import asyncio
import aiodocker
import json
from app.core.db import db_deps
from app.models.logs import SystemContainerLog
from common.logger import get_logger

logger = get_logger(__name__)

async def docker_event_listener():
    while True:
        docker = aiodocker.Docker()
        try:
            logger.info("Rozpoczęto pasywne nasłuchiwanie zdarzeń Docker w tle...")
            subscriber = docker.events.subscribe()
            
            while True:
                event = await subscriber.get()
                
                if event is None:
                    break
                
                if event.get("Type") == "container":
                    action = event.get("Action", "")

                    if action in ["die", "stop", "oom"] or "health_status: unhealthy" in action:
                        attributes = event.get("Actor", {}).get("Attributes", {})
                        container_name = attributes.get("name", "unknown")
                        
                        if container_name.startswith("homeos-"):
                            logger.warning(f"🚨 ANOMALIA: Kontener '{container_name}' zgłosił: {action}")
                            
                            async for db in db_deps.get_session():
                                try:
                                    log_entry = SystemContainerLog(
                                        container_name=container_name,
                                        event_type=action,
                                        details=json.dumps(attributes)
                                    )
                                    db.add(log_entry)
                                    await db.commit()
                                except Exception as db_err:
                                    logger.error(f"Błąd podczas zapisu logu do bazy: {db_err}")
                                break 
                                
        except asyncio.CancelledError:
            logger.info("Nasłuchiwacz Dockera został poprawnie zatrzymany.")
            break
            
        except Exception as e:
            logger.error(f"Utracono połączenie z gniazdem Dockera: {e}. Ponawiam za 5 sekund...")
            await asyncio.sleep(5)
            
        finally:
            await docker.close()