from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.repository import Repository
from app.schemas.dashboard import AgentStatus, DashboardSummary
from app.schemas.repository import RepositoryRead


PLANNED_AGENTS = [
    AgentStatus(
        id="security",
        name="Security Agent",
        status="not_implemented",
        description="Will scan for vulnerabilities, secrets, and insecure patterns.",
    ),
    AgentStatus(
        id="repository-intelligence",
        name="Repository Intelligence Agent",
        status="not_implemented",
        description="Will map architecture, ownership, and change hotspots.",
    ),
    AgentStatus(
        id="code-quality",
        name="Code Quality Agent",
        status="not_implemented",
        description="Will measure complexity, duplication, and maintainability.",
    ),
    AgentStatus(
        id="dependency",
        name="Dependency Agent",
        status="not_implemented",
        description="Will inspect dependency health and known advisories.",
    ),
    AgentStatus(
        id="refactoring",
        name="Refactoring Agent",
        status="not_implemented",
        description="Will propose and apply guarded structural changes.",
    ),
    AgentStatus(
        id="predictive-maintenance",
        name="Predictive Maintenance Agent",
        status="not_implemented",
        description="Will forecast defect and churn risk from history.",
    ),
    AgentStatus(
        id="orchestrator",
        name="Autonomous Orchestrator",
        status="not_implemented",
        description="Will coordinate agent runs, validation, and rollback.",
    ),
    AgentStatus(
        id="validation",
        name="Validation / Test Agent",
        status="not_implemented",
        description="Will verify changes with tests before promotion.",
    ),
    AgentStatus(
        id="rollback",
        name="Rollback System",
        status="not_implemented",
        description="Will restore a known-good state if validation fails.",
    ),
    AgentStatus(
        id="reporting",
        name="Reporting Agent",
        status="not_implemented",
        description="Will produce audit-ready engineering reports.",
    ),
]


def get_dashboard_summary(db: Session) -> DashboardSummary:
    count = db.scalar(select(func.count()).select_from(Repository)) or 0
    recent = list(db.scalars(select(Repository).order_by(Repository.created_at.desc()).limit(5)).all())
    return DashboardSummary(
        service=settings.app_name,
        version=settings.app_version,
        system_status="operational",
        repository_count=count,
        analysis_runs=0,
        agents=PLANNED_AGENTS,
        recent_repositories=[RepositoryRead.model_validate(item) for item in recent],
        notice=(
            "No analysis has been run. Register a repository to prepare the workspace. "
            "Security, quality, refactoring, and prediction agents are not implemented in this foundation stage."
        ),
    )
