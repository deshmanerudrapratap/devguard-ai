from pathlib import Path

from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class RefactoringAgent(BaseAgent):
    agent_id = "refactoring"
    name = "Refactoring Agent"
    status = AgentStatus.READY

    SOURCE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx"}

    def run(self, context: AgentContext) -> AgentResult:
        repository_path = Path(context.local_path)

        if not repository_path.exists():
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                message="Repository path does not exist.",
                payload={
                    "repository_id": context.repository_id,
                    "recommendations": [],
                },
            )

        recommendations = []
        scanned_files = 0

        for file_path in repository_path.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in self.SOURCE_EXTENSIONS:
                continue

            scanned_files += 1

            try:
                lines = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).splitlines()

                for line_number, line in enumerate(lines, start=1):
                    stripped = line.strip()

                    if "TODO" in stripped or "FIXME" in stripped:
                        recommendations.append({
                            "file": str(
                                file_path.relative_to(repository_path)
                            ),
                            "line": line_number,
                            "type": "INCOMPLETE_IMPLEMENTATION",
                            "message": "Replace TODO/FIXME with a completed implementation.",
                        })

                    if file_path.suffix == ".py" and stripped.startswith("print("):
                        recommendations.append({
                            "file": str(
                                file_path.relative_to(repository_path)
                            ),
                            "line": line_number,
                            "type": "REPLACE_PRINT",
                            "message": "Consider replacing print statements with structured logging.",
                        })

                    if len(line) > 120:
                        recommendations.append({
                            "file": str(
                                file_path.relative_to(repository_path)
                            ),
                            "line": line_number,
                            "type": "LONG_LINE",
                            "message": "Consider breaking this long line into smaller statements.",
                        })

            except Exception:
                continue

        refactoring_status = (
            "NO_REFACTORING_NEEDED"
            if len(recommendations) == 0
            else "REFACTORING_RECOMMENDED"
        )

        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.READY,
            message=(
                f"Refactoring analysis completed. "
                f"{len(recommendations)} recommendations found."
            ),
            payload={
                "repository": context.repository_name,
                "scanned_files": scanned_files,
                "total_recommendations": len(recommendations),
                "status": refactoring_status,
                "recommendations": recommendations,
                "execution_mode": "SUGGEST_ONLY",
            },
        )