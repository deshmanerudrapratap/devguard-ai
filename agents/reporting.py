from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class ReportingAgent(BaseAgent):
    agent_id = "reporting"
    name = "Reporting Agent"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Reporting Agent is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
