from agents.base import AgentContext, AgentResult, AgentStatus, BaseAgent


class CodeQualityAgent(BaseAgent):
    agent_id = "code-quality"
    name = "Code Quality Agent"
    status = AgentStatus.NOT_IMPLEMENTED

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(
            agent_id=self.agent_id,
            status=AgentStatus.NOT_IMPLEMENTED,
            message="Code Quality Agent is not implemented yet.",
            payload={"repository_id": context.repository_id},
        )
