from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class ValidationAgent(BaseAgent):
    agent_id = "validation"
    name = "Validation / Test Agent"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Validation / Test Agent is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
