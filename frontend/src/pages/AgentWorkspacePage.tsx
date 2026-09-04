import { api } from "../api/client"
import { AgentEmptyPanel } from "../components/AgentEmptyPanel"
import { AppShell } from "../components/layout/AppShell"
import { Card } from "../components/ui/Card"
import { ErrorBanner } from "../components/ui/ErrorBanner"
import { LoadingState } from "../components/ui/LoadingState"
import { StatusPill } from "../components/ui/StatusPill"
import { useAsync } from "../hooks/useAsync"

type Props = {
  title: string
  subtitle: string
  agentId: string
  capability: string
}

export function AgentWorkspacePage({ title, subtitle, agentId, capability }: Props) {
  const health = useAsync(() => api.health(), [])
  const summary = useAsync(() => api.dashboardSummary(), [])
  const agent = summary.data?.agents.find((item) => item.id === agentId)

  return (
    <AppShell title={title} subtitle={subtitle} health={health.data?.status}>
      <div className="grid gap-5">
        {summary.loading ? <LoadingState /> : null}
        {summary.error ? <ErrorBanner message={summary.error} onRetry={() => void summary.reload()} /> : null}

        <Card title="Agent contract">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="font-medium text-slate-100">{agent?.name ?? title}</p>
              <p className="mt-1 text-sm text-slate-400">{agent?.description ?? capability}</p>
            </div>
            <StatusPill status={agent?.status ?? "not_implemented"} />
          </div>
        </Card>

        <AgentEmptyPanel agentName={agent?.name ?? title} capability={capability} />
      </div>
    </AppShell>
  )
}
