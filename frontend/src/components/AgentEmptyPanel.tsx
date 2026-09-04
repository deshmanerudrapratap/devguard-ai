import { EmptyState } from "./ui/EmptyState"

type Props = {
  agentName: string
  capability: string
}

export function AgentEmptyPanel({ agentName, capability }: Props) {
  return (
    <EmptyState
      title={`${agentName} is not implemented yet`}
      description={`${capability} No findings, scores, or recommendations are shown because this agent has not been built. The UI is ready to display real results when the agent is connected.`}
    />
  )
}
