from app.services.telemetry import get_system_metrics
from app.core.exceptions import FailedToGetSystemMetricsException
import json
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import db_deps
from app.core.user import AdminUser
from app.models.logs import SystemContainerLog

router = APIRouter(prefix="/dashboard", tags=["System Dashboard"])

@router.get("/")
def get_dashboard(user: AdminUser):
    
    return get_system_metrics()

@router.get("/logs")
async def get_system_container_logs(
    user: AdminUser,
    session: AsyncSession = Depends(db_deps.get_session),
    limit: int = Query(default=20, ge=1, le=100, description="Liczba ostatnich logów do pobrania"),
    container_name: Optional[str] = Query(default=None, description="Filtruj logi po nazwie kontenera")
):
    """
    Pobiera historię zdarzeń i anomalii kontenerów zapisanych w bazie danych.
    Pozwala na budowanie osi czasu (Timeline) zdarzeń w panelu administracyjnym.
    """
    try:
        query = select(SystemContainerLog).order_by(desc(SystemContainerLog.created_at))

        if container_name:
            query = query.where(SystemContainerLog.container_name == container_name)

        query = query.limit(limit)

        result = await session.exec(query)
        logs = result.all()

        formatted_logs = []
        for log in logs:
            parsed_details = None
            if log.details:
                try:
                    parsed_details = json.loads(log.details)
                except json.JSONDecodeError:
                    parsed_details = log.details

            formatted_logs.append({
                "id": log.id,
                "container_name": log.container_name,
                "event_type": log.event_type,
                "details": parsed_details,
                "created_at": log.created_at
            })

        return {
            "status": "success",
            "count": len(formatted_logs),
            "data": formatted_logs
        }

    except Exception as e:
        raise FailedToGetSystemMetricsException()