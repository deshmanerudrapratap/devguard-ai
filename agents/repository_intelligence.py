from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class RepositoryIntelligenceAgent(BaseAgent):
    agent_id = "repository-intelligence"
    name = "Repository Intelligence Agent"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Repository Intelligence Agent is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
