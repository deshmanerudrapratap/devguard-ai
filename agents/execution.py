from pathlib import Path
import shutil
import uuid

from agents.base import (
    AgentContext,
    AgentResult,
    AgentStatus,
    BaseAgent,
)


class ExecutionAgent(BaseAgent):
    """
    Safe execution layer for DevGuard AI.

    Every modification requires explicit approval.
    Before modification, a backup is created so the
    operation can be rolled back.
    """

    agent_id = "execution"
    name = "Approval, Execution & Rollback Agent"
    status = AgentStatus.READY

    def _get_root(self, context: AgentContext) -> Path:
        if context.local_path:
            path = Path(context.local_path)

            if path.exists():
                return path.resolve()

        return (
            Path(__file__).resolve().parent.parent
            / "demo-target"
        ).resolve()

    def create_backup(self, repository_path: Path):
        backup_root = (
            repository_path.parent
            / ".devguard_backups"
        )

        backup_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_id = str(uuid.uuid4())[:8]

        backup_path = (
            backup_root
            / f"{repository_path.name}_{backup_id}"
        )

        shutil.copytree(
            repository_path,
            backup_path,
            ignore=shutil.ignore_patterns(
                ".git",
                ".venv",
                "node_modules",
                "__pycache__",
                ".pytest_cache",
                ".devguard_backups",
            ),
        )

        return backup_path

    def execute_file_change(
        self,
        repository_path: Path,
        relative_file: str,
        new_content: str,
        approved: bool,
    ):
        if not approved:
            return {
                "status": "WAITING_FOR_APPROVAL",
                "message": (
                    "Change was not executed because "
                    "human approval is required."
                ),
            }

        target = (
            repository_path / relative_file
        ).resolve()

        # Security: prevent writing outside repository
        if repository_path not in target.parents:
            raise ValueError(
                "Unsafe file path: modification "
                "outside repository is not allowed."
            )

        backup_path = self.create_backup(
            repository_path
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            new_content,
            encoding="utf-8",
        )

        return {
            "status": "EXECUTED",
            "file": relative_file,
            "backup": str(backup_path),
            "message": (
                "Approved change executed successfully "
                "and backup created."
            ),
        }

    def rollback(
        self,
        repository_path: Path,
        backup_path: str,
    ):
        backup = Path(backup_path)

        if not backup.exists():
            raise FileNotFoundError(
                "Backup does not exist."
            )

        if repository_path.exists():
            shutil.rmtree(repository_path)

        shutil.copytree(
            backup,
            repository_path,
        )

        return {
            "status": "ROLLED_BACK",
            "message": (
                "Repository successfully restored "
                "from backup."
            ),
            "backup": str(backup),
        }

    def run(self, context: AgentContext) -> AgentResult:
        try:
            repository_path = self._get_root(context)

            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.READY,
                message=(
                    "Execution system ready. "
                    "Human approval is required before "
                    "any repository modification."
                ),
                payload={
                    "repository": repository_path.name,
                    "repository_path": str(
                        repository_path
                    ),
                    "approval_required": True,
                    "rollback_supported": True,
                    "safe_execution": True,
                },
            )

        except Exception as exc:
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                message=f"Execution system failed: {exc}",
                payload={
                    "repository_id": context.repository_id,
                    "error": str(exc),
                },
            )