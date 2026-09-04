from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class RollbackSystem(BaseAgent):
    agent_id = "rollback"
    name = "Rollback System"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Rollback system is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
