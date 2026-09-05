from pathlib import Path
import re

from agents.base import (
    AgentContext,
    AgentResult,
    AgentStatus,
    BaseAgent,
)


class SecurityAgent(BaseAgent):
    agent_id = "security-scanner"
    name = "Security/API Scanner"
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

    FILE_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".php",
        ".rb",
        ".go",
        ".cs",
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

    def _is_ignored(self, path: Path) -> bool:
        return any(
            part in self.IGNORE_DIRS
            for part in path.parts
        )

    def _scan_file(self, file_path: Path, root: Path):
        findings = []

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            return findings

        relative_path = str(file_path.relative_to(root))

        patterns = [
            (
                r"(?i)(password|passwd)\s*=\s*[\"'][^\"']+[\"']",
                "Hardcoded password detected",
                "HIGH",
            ),
            (
                r"(?i)(api[_-]?key|secret[_-]?key)\s*=\s*[\"'][^\"']+[\"']",
                "Possible hardcoded API key or secret detected",
                "HIGH",
            ),
            (
                r"(?i)(token|auth[_-]?token)\s*=\s*[\"'][^\"']+[\"']",
                "Possible hardcoded authentication token detected",
                "HIGH",
            ),
            (
                r"(?i)debug\s*=\s*true",
                "Debug mode appears to be enabled",
                "MEDIUM",
            ),
            (
                r"(?i)verify\s*=\s*false",
                "TLS/SSL certificate verification disabled",
                "HIGH",
            ),
            (
                r"(?i)http://",
                "Unencrypted HTTP URL detected",
                "MEDIUM",
            ),
            (
                r"(?i)subprocess\.(run|call|Popen)\s*\(",
                "Subprocess execution detected; review command injection risk",
                "MEDIUM",
            ),
            (
                r"(?i)eval\s*\(",
                "Dynamic eval() execution detected",
                "HIGH",
            ),
            (
                r"(?i)exec\s*\(",
                "Dynamic exec() execution detected",
                "HIGH",
            ),
        ]

        lines = content.splitlines()

        for line_number, line in enumerate(lines, start=1):
            for pattern, message, severity in patterns:
                if re.search(pattern, line):
                    findings.append(
                        {
                            "file": relative_path,
                            "line": line_number,
                            "severity": severity,
                            "message": message,
                            "evidence": line.strip()[:200],
                        }
                    )

        return findings

    def scan_repository(self, root: Path):
        findings = []
        scanned_files = 0

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue

            if self._is_ignored(file_path):
                continue

            if file_path.suffix.lower() not in self.FILE_EXTENSIONS:
                continue

            scanned_files += 1

            findings.extend(
                self._scan_file(
                    file_path,
                    root,
                )
            )

        severity_counts = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for finding in findings:
            severity = finding["severity"]

            if severity in severity_counts:
                severity_counts[severity] += 1

        risk_score = (
            severity_counts["HIGH"] * 10
            + severity_counts["MEDIUM"] * 5
            + severity_counts["LOW"] * 2
        )

        if risk_score == 0:
            security_status = "SECURE"
        elif risk_score < 20:
            security_status = "LOW RISK"
        elif risk_score < 50:
            security_status = "MEDIUM RISK"
        else:
            security_status = "HIGH RISK"

        return {
            "repository": root.name,
            "path": str(root),
            "scanned_files": scanned_files,
            "total_findings": len(findings),
            "severity": severity_counts,
            "risk_score": risk_score,
            "security_status": security_status,
            "findings": findings,
        }

    def run(self, context: AgentContext) -> AgentResult:
        try:
            repository_path = self._get_repository_path(context)

            result = self.scan_repository(
                repository_path
            )

            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.READY,
                message="Security scan completed successfully.",
                payload=result,
            )

        except Exception as exc:
            return AgentResult(
                agent_id=self.agent_id,
                status=AgentStatus.FAILED,
                message=f"Security scan failed: {exc}",
                payload={
                    "repository_id": context.repository_id,
                    "error": str(exc),
                },
            )