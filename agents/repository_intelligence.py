from pathlib import Path
from collections import Counter

from agents.base import (
    AgentContext,
    AgentResult,
    AgentStatus,
    BaseAgent,
)


class RepositoryIntelligenceAgent(BaseAgent):
    agent_id = "repository-intelligence"
    name = "Repository Intelligence Agent"
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

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".html": "HTML",
        ".css": "CSS",
        ".sql": "SQL",
    }

    DEPENDENCY_FILES = {
        "requirements.txt",
        "package.json",
        "package-lock.json",
        "pyproject.toml",
        "pom.xml",
        "go.mod",
        "Cargo.toml",
    }

    def _get_repository_path(self, context: AgentContext) -> Path:
        """
        Find repository path from AgentContext.
        Supports several possible context field names so the
        agent remains compatible with the existing foundation.
        """

        possible_fields = [
            "repository_path",
            "repo_path",
            "workspace_path",
            "path",
            "repository",
        ]

        for field in possible_fields:
            value = getattr(context, field, None)

            if value:
                path = Path(str(value))

                if path.exists():
                    return path.resolve()

        # Fallback to project/demo repository
        project_root = Path(__file__).resolve().parent.parent

        demo_target = project_root / "demo-target"

        if demo_target.exists():
            return demo_target.resolve()

        return project_root.resolve()

    def _is_ignored(self, path: Path) -> bool:
        return any(
            part in self.IGNORE_DIRS
            for part in path.parts
        )

    def _count_lines(self, path: Path) -> int:
        try:
            with open(
                path,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                return sum(1 for _ in file)
        except Exception:
            return 0

    def _get_files(self, root: Path):
        return [
            file
            for file in root.rglob("*")
            if file.is_file()
            and not self._is_ignored(file)
        ]

    def analyze_repository(self, root: Path):
        files = self._get_files(root)

        languages = Counter()
        dependency_files = []
        important_files = []
        file_details = []

        total_lines = 0

        for file in files:
            relative_path = file.relative_to(root)
            line_count = self._count_lines(file)

            total_lines += line_count

            extension = file.suffix.lower()

            if extension in self.LANGUAGE_MAP:
                languages[self.LANGUAGE_MAP[extension]] += 1

            if file.name in self.DEPENDENCY_FILES:
                dependency_files.append(
                    str(relative_path)
                )

            if file.name.lower() in {
                "readme.md",
                "requirements.txt",
                "package.json",
                "pyproject.toml",
                "dockerfile",
                ".gitignore",
            }:
                important_files.append(
                    str(relative_path)
                )

            file_details.append(
                {
                    "file": str(relative_path),
                    "lines": line_count,
                    "extension": extension,
                }
            )

        file_details.sort(
            key=lambda item: item["lines"],
            reverse=True,
        )

        directories = {
            str(file.relative_to(root).parent)
            for file in files
            if str(file.relative_to(root).parent) != "."
        }

        # Repository health calculation
        health_score = 100

        if not files:
            health_score -= 50

        if not dependency_files:
            health_score -= 10

        if total_lines == 0:
            health_score -= 20

        if not important_files:
            health_score -= 10

        health_score = max(
            0,
            min(100, health_score),
        )

        if health_score >= 80:
            health_status = "Healthy"
        elif health_score >= 60:
            health_status = "Needs Attention"
        else:
            health_status = "Critical"

        return {
            "repository": root.name,
            "path": str(root),
            "total_files": len(files),
            "total_directories": len(directories),
            "total_lines": total_lines,
            "languages": dict(languages),
            "dependency_files": dependency_files,
            "important_files": important_files,
            "largest_files": file_details[:10],
            "health": {
                "score": health_score,
                "status": health_status,
            },
        }

    def run(self, context: AgentContext) -> AgentResult:
        try:
            repository_path = self._get_repository_path(context)

            analysis = self.analyze_repository(
                repository_path
            )

            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.READY,
                message=(
                    "Repository analysis completed successfully."
                ),
                payload=analysis,
            )

        except Exception as exc:
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                message=(
                    f"Repository analysis failed: {exc}"
                ),
                payload={
                    "repository_id": context.repository_id,
                    "error": str(exc),
                },
            )