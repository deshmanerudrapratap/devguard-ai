from pathlib import Path
from datetime import datetime

from agents.base import (
    AgentContext,
    AgentResult,
    AgentStatus,
    BaseAgent,
)


class PredictiveMaintenanceAgent(BaseAgent):
    agent_id = "predictive-maintenance"
    name = "Predictive Maintenance Agent"
    status = AgentStatus.READY

    IGNORE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        "dist",
        "build",
    }

    def _get_repository_path(self, context: AgentContext) -> Path:
        if context.local_path:
            path = Path(context.local_path)

            if path.exists():
                return path.resolve()

        project_root = Path(__file__).resolve().parent.parent
        demo_target = project_root / "demo-target"

        if demo_target.exists():
            return demo_target.resolve()

        return project_root.resolve()

    def _ignored(self, path: Path) -> bool:
        return any(
            part in self.IGNORE_DIRS
            for part in path.parts
        )

    def _collect_metrics(self, root: Path):
        files = []
        total_lines = 0
        large_files = 0
        todo_count = 0
        source_files = 0

        source_extensions = {
            ".py", ".js", ".jsx", ".ts", ".tsx",
            ".java", ".c", ".cpp", ".cs",
            ".go", ".php", ".rb"
        }

        for path in root.rglob("*"):
            if not path.is_file() or self._ignored(path):
                continue

            files.append(path)

            if path.suffix.lower() in source_extensions:
                source_files += 1

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except Exception:
                continue

            lines = content.splitlines()
            line_count = len(lines)

            total_lines += line_count

            if line_count > 300:
                large_files += 1

            for line in lines:
                if "TODO" in line.upper() or "FIXME" in line.upper():
                    todo_count += 1

        return {
            "total_files": len(files),
            "source_files": source_files,
            "total_lines": total_lines,
            "large_files": large_files,
            "todo_count": todo_count,
        }

    def _calculate_risk(self, metrics):
        risk_score = 0

        # Large repositories are more difficult to maintain.
        if metrics["total_files"] > 100:
            risk_score += 15
        elif metrics["total_files"] > 50:
            risk_score += 10

        if metrics["total_lines"] > 10000:
            risk_score += 20
        elif metrics["total_lines"] > 5000:
            risk_score += 10

        # Large files increase maintenance risk.
        risk_score += min(
            metrics["large_files"] * 5,
            20,
        )

        # TODO/FIXME backlog.
        risk_score += min(
            metrics["todo_count"] * 2,
            20,
        )

        risk_score = min(100, risk_score)

        if risk_score >= 70:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return risk_score, risk_level

    def _generate_predictions(self, metrics, risk_score):
        predictions = []
        recommendations = []

        if metrics["large_files"] > 0:
            predictions.append(
                "Large source files may become future maintenance bottlenecks."
            )
            recommendations.append(
                "Consider splitting large files into smaller modules."
            )

        if metrics["todo_count"] > 0:
            predictions.append(
                "Outstanding TODO/FIXME items may increase future technical debt."
            )
            recommendations.append(
                "Prioritize unresolved TODO/FIXME items."
            )

        if metrics["total_lines"] > 5000:
            predictions.append(
                "Growing code volume may increase maintenance effort."
            )
            recommendations.append(
                "Introduce regular refactoring and code-quality checks."
            )

        if risk_score < 40:
            predictions.append(
                "Current repository structure shows relatively low maintenance risk."
            )
            recommendations.append(
                "Continue automated monitoring to detect future degradation."
            )

        return predictions, recommendations

    def analyze_repository(self, root: Path):
        metrics = self._collect_metrics(root)

        risk_score, risk_level = self._calculate_risk(
            metrics
        )

        predictions, recommendations = (
            self._generate_predictions(
                metrics,
                risk_score,
            )
        )

        return {
            "repository": root.name,
            "path": str(root),
            "analysis_time": datetime.now().isoformat(),
            "metrics": metrics,
            "maintenance_risk": {
                "score": risk_score,
                "level": risk_level,
            },
            "predictions": predictions,
            "recommendations": recommendations,
            "status": (
                "ACTION_REQUIRED"
                if risk_score >= 40
                else "STABLE"
            ),
        }

    def run(self, context: AgentContext) -> AgentResult:
        try:
            repository_path = self._get_repository_path(
                context
            )

            result = self.analyze_repository(
                repository_path
            )

            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.READY,
                message=(
                    "Predictive maintenance analysis "
                    "completed successfully."
                ),
                payload=result,
            )

        except Exception as exc:
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                message=(
                    f"Predictive maintenance analysis failed: {exc}"
                ),
                payload={
                    "repository_id": context.repository_id,
                    "error": str(exc),
                },
            )