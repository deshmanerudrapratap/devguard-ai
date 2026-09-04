from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class AutonomousOrchestrator(BaseAgent):
    agent_id = "orchestrator"
    name = "Autonomous Orchestrator"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Autonomous Orchestrator is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
