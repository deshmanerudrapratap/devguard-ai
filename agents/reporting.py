from datetime import datetime

from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent
from agents.repository_intelligence import RepositoryIntelligenceAgent
from agents.security import SecurityAgent
from agents.code_quality import CodeQualityAgent
from agents.predictive_maintenance import PredictiveMaintenanceAgent
from agents.refactoring import RefactoringAgent


class ReportingAgent(BaseAgent):
    agent_id = "reporting"
    name = "Reporting Agent"
    status = AgentStatus.READY

    def run(self, context: AgentContext) -> AgentResult:
        agents = [
            RepositoryIntelligenceAgent(),
            SecurityAgent(),
            CodeQualityAgent(),
            PredictiveMaintenanceAgent(),
            RefactoringAgent(),
        ]

        agent_results = []
        completed = 0
        failed = 0

        for agent in agents:
            try:
                result = agent.run(context)

                agent_results.append({
                    "agent_id": result.agent_id,
                    "agent_name": agent.name,
                    "status": result.status.value,
                    "message": result.message,
                    "payload": result.payload,
                })

                if result.status == AgentStatus.FAILED:
                    failed += 1
                else:
                    completed += 1

            except Exception as exc:
                failed += 1

                agent_results.append({
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "status": "FAILED",
                    "message": str(exc),
                    "payload": {},
                })

        report_status = (
            "COMPLETED"
            if failed == 0
            else "PARTIAL"
            if completed > 0
            else "FAILED"
        )

        return AgentResult(
            agent_id=self.agent_id,
            status=(
                AgentStatus.READY
                if completed > 0
                else AgentStatus.FAILED
            ),
            message=(
                f"Engineering report generated: "
                f"{completed} agents completed, "
                f"{failed} failed."
            ),
            payload={
                "repository_id": context.repository_id,
                "repository_name": context.repository_name,
                "generated_at": datetime.now().isoformat(),
                "report_status": report_status,
                "agents_analyzed": len(agents),
                "agents_completed": completed,
                "agents_failed": failed,
                "agent_results": agent_results,
                "summary": {
                    "message": (
                        "DevGuard AI engineering analysis report "
                        "generated successfully."
                    ),
                },
            },
        )