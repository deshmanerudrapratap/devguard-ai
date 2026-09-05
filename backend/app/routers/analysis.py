from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.orchestrator import AutonomousOrchestrator
from agents.base import AgentContext

router = APIRouter(prefix="/analysis", tags=["analysis"])


class AnalysisRequest(BaseModel):
    repository_id: int
    repository_name: str
    local_path: str


@router.post("/run")
def run_analysis(payload: AnalysisRequest):
    repository_path = Path(payload.local_path).resolve()

    if not repository_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Repository path not found: {repository_path}",
        )

    context = AgentContext(
        repository_id=payload.repository_id,
        repository_name=payload.repository_name,
        local_path=str(repository_path),
    )

    try:
        result = AutonomousOrchestrator().run(context)

        return {
            "status": result.status.value,
            "message": result.message,
            "payload": result.payload,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        ) from exc