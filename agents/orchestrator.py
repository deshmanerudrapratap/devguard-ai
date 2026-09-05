from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent
from agents.repository_intelligence import RepositoryIntelligenceAgent
from agents.security import SecurityAgent
from agents.code_quality import CodeQualityAgent
from agents.predictive_maintenance import PredictiveMaintenanceAgent


class AutonomousOrchestrator(BaseAgent):
    agent_id = "orchestrator"
    name = "Autonomous Orchestrator"
    status = AgentStatus.READY

    def run(self, context: AgentContext) -> AgentResult:
        agents = [
            RepositoryIntelligenceAgent(),
            SecurityAgent(),
            CodeQualityAgent(),
            PredictiveMaintenanceAgent(),
        ]

        results = []
        completed = 0
        failed = 0

        for agent in agents:
            try:
                result = agent.run(context)

                results.append({
                    "agent_id": result.agent_id,
                    "status": result.status.value,
                    "message": result.message,
                    "payload": result.payload,
                })

                if result.status != AgentStatus.FAILED:
                    completed += 1
                else:
                    failed += 1

            except Exception as exc:
                failed += 1
                results.append({
                    "agent_id": agent.agent_id,
                    "status": AgentStatus.FAILED.value,
                    "message": str(exc),
                    "payload": {},
                })

        overall_status = (
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
                if failed == 0
                else AgentStatus.FAILED
            ),
            message=(
                f"Orchestration finished: "
                f"{completed} agents completed, "
                f"{failed} failed."
            ),
            payload={
                "repository_id": context.repository_id,
                "overall_status": overall_status,
                "agents_executed": len(agents),
                "agents_completed": completed,
                "agents_failed": failed,
                "results": results,
            },
        )