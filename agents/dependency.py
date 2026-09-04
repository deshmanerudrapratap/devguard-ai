from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class DependencyAgent(BaseAgent):
    agent_id = "dependency"
    name = "Dependency Agent"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Dependency Agent is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
