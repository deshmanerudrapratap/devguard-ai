from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def healthcheck(db: Session = Depends(get_db)) -> HealthResponse:
    database_status = "disconnected"
    try:
        db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception:
        database_status = "error"

    overall = "ok" if database_status == "connected" else "degraded"
    return HealthResponse(
        status=overall,
        service=settings.app_name,
        version=settings.app_version,
        database=database_status,
    )
