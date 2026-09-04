from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class RefactoringAgent(BaseAgent):
    agent_id = "refactoring"
    name = "Refactoring Agent"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Refactoring Agent is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
