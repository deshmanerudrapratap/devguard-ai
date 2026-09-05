from pathlib import Path
import re

from agents.base import (
    AgentContext,
    AgentResult,
    AgentStatus,
    BaseAgent,
)


class CodeQualityAgent(BaseAgent):
    agent_id = "code-quality"
    name = "Code Quality & Refactoring Agent"
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

    SOURCE_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".cs",
        ".go",
        ".php",
        ".rb",
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

    def _read_file(self, path: Path):
        try:
            return path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            return ""

    def _analyze_file(self, file_path: Path, root: Path):
        content = self._read_file(file_path)

        if not content:
            return []

        findings = []
        lines = content.splitlines()
        relative = str(file_path.relative_to(root))

        for number, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Long line
            if len(line) > 120:
                findings.append({
                    "file": relative,
                    "line": number,
                    "type": "LONG_LINE",
                    "severity": "LOW",
                    "message": "Line exceeds 120 characters.",
                })

            # TODO / FIXME
            if re.search(r"\b(TODO|FIXME)\b", line, re.IGNORECASE):
                findings.append({
                    "file": relative,
                    "line": number,
                    "type": "TODO",
                    "severity": "LOW",
                    "message": "Pending TODO/FIXME item found.",
                })

            # Python print statements
            if file_path.suffix.lower() == ".py":
                if re.search(r"^\s*print\s*\(", line):
                    findings.append({
                        "file": relative,
                        "line": number,
                        "type": "PRINT_STATEMENT",
                        "severity": "LOW",
                        "message": "Print statement found; consider structured logging.",
                    })

                # Bare except
                if re.match(r"^\s*except\s*:", line):
                    findings.append({
                        "file": relative,
                        "line": number,
                        "type": "BARE_EXCEPT",
                        "severity": "MEDIUM",
                        "message": "Bare except can hide unexpected errors.",
                    })

                # Mutable default argument
                if re.search(
                    r"def\s+\w+\s*\([^)]*=\s*(\[\]|\{\})",
                    line,
                ):
                    findings.append({
                        "file": relative,
                        "line": number,
                        "type": "MUTABLE_DEFAULT",
                        "severity": "MEDIUM",
                        "message": "Mutable default argument detected.",
                    })

        return findings

    def analyze_repository(self, root: Path):
        findings = []
        scanned_files = 0
        total_lines = 0

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue

            if self._ignored(file_path):
                continue

            if file_path.suffix.lower() not in self.SOURCE_EXTENSIONS:
                continue

            scanned_files += 1

            content = self._read_file(file_path)

            total_lines += len(content.splitlines())

            findings.extend(
                self._analyze_file(
                    file_path,
                    root,
                )
            )

        severity = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for finding in findings:
            level = finding["severity"]

            if level in severity:
                severity[level] += 1

        # Quality score
        score = 100

        score -= severity["HIGH"] * 10
        score -= severity["MEDIUM"] * 5
        score -= severity["LOW"] * 2

        score = max(0, min(100, score))

        if score >= 85:
            status = "EXCELLENT"
        elif score >= 70:
            status = "GOOD"
        elif score >= 50:
            status = "NEEDS IMPROVEMENT"
        else:
            status = "POOR"

        return {
            "repository": root.name,
            "path": str(root),
            "scanned_files": scanned_files,
            "total_lines": total_lines,
            "total_findings": len(findings),
            "severity": severity,
            "quality_score": score,
            "quality_status": status,
            "findings": findings,
            "refactoring_recommendations": self._recommendations(
                findings
            ),
        }

    def _recommendations(self, findings):
        recommendations = []

        types = {
            finding["type"]
            for finding in findings
        }

        if "LONG_LINE" in types:
            recommendations.append(
                "Break long lines into smaller readable expressions."
            )

        if "TODO" in types:
            recommendations.append(
                "Review and resolve outstanding TODO/FIXME items."
            )

        if "PRINT_STATEMENT" in types:
            recommendations.append(
                "Replace print statements with application logging."
            )

        if "BARE_EXCEPT" in types:
            recommendations.append(
                "Replace bare except blocks with specific exceptions."
            )

        if "MUTABLE_DEFAULT" in types:
            recommendations.append(
                "Use None and initialize mutable values inside functions."
            )

        if not recommendations:
            recommendations.append(
                "No major automatic refactoring recommendations found."
            )

        return recommendations

    def run(self, context: AgentContext) -> AgentResult:
        try:
            repository_path = self._get_repository_path(context)

            result = self.analyze_repository(
                repository_path
            )

            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.READY,
                message="Code quality analysis completed successfully.",
                payload=result,
            )

        except Exception as exc:
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                message=f"Code quality analysis failed: {exc}",
                payload={
                    "repository_id": context.repository_id,
                    "error": str(exc),
                },
            )