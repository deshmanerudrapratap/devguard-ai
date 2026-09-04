from pydantic import BaseModel

from app.schemas.repository import RepositoryRead


class AgentStatus(BaseModel):
    id: str
    name: str
    status: str
    description: str


class DashboardSummary(BaseModel):
    service: str
    version: str
    system_status: str
    repository_count: int
    analysis_runs: int
    agents: list[AgentStatus]
    recent_repositories: list[RepositoryRead]
    notice: str
