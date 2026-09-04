import { useMemo, useState } from "react"
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import { api } from "../api/client"
import type { RepositoryPayload } from "../api/types"
import { AgentEmptyPanel } from "../components/AgentEmptyPanel"
import { AppShell } from "../components/layout/AppShell"
import { RepositoryForm } from "../components/RepositoryForm"
import { RepositoryTable } from "../components/RepositoryTable"
import { Card } from "../components/ui/Card"
import { ErrorBanner } from "../components/ui/ErrorBanner"
import { LoadingState } from "../components/ui/LoadingState"
import { StatusPill } from "../components/ui/StatusPill"
import { SuccessBanner } from "../components/ui/SuccessBanner"
import { useAsync } from "../hooks/useAsync"

export function OverviewPage() {
  const health = useAsync(() => api.health(), [])
  const summary = useAsync(() => api.dashboardSummary(), [])
  const repos = useAsync(() => api.listRepositories(), [])
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess] = useState<string | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)

  const chartData = useMemo(() => {
    const counts = new Map<string, number>()
    for (const repo of repos.data ?? []) {
      const day = new Date(repo.created_at).toLocaleDateString()
      counts.set(day, (counts.get(day) ?? 0) + 1)
    }
    return [...counts.entries()].map(([day, count]) => ({ day, count }))
  }, [repos.data])

  async function register(payload: RepositoryPayload) {
    setSubmitting(true)
    setActionError(null)
    setSuccess(null)
    try {
      const created = await api.createRepository(payload)
      setSuccess(`Registered ${created.name}. No analysis has been run.`)
      await Promise.all([summary.reload(), repos.reload()])
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "Registration failed")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AppShell
      title="Overview"
      subtitle="Operational status of the DevGuard AI command center"
      health={health.data?.status}
    >
      <div className="grid gap-5">
        {health.loading || summary.loading || repos.loading ? (
          <LoadingState />
        ) : null}
        {health.error ? <ErrorBanner message={health.error} onRetry={() => void health.reload()} /> : null}
        {summary.error ? <ErrorBanner message={summary.error} onRetry={() => void summary.reload()} /> : null}
        {repos.error ? <ErrorBanner message={repos.error} onRetry={() => void repos.reload()} /> : null}
        {actionError ? <ErrorBanner message={actionError} /> : null}
        {success ? <SuccessBanner message={success} /> : null}

        <div className="grid gap-5 md:grid-cols-4">
          <Card>
            <p className="text-xs uppercase tracking-wide text-slate-500">Service</p>
            <p className="mt-2 text-lg font-semibold text-white">{summary.data?.service ?? "—"}</p>
          </Card>
          <Card>
            <p className="text-xs uppercase tracking-wide text-slate-500">Repositories</p>
            <p className="mt-2 text-lg font-semibold text-white">{summary.data?.repository_count ?? 0}</p>
          </Card>
          <Card>
            <p className="text-xs uppercase tracking-wide text-slate-500">Analysis runs</p>
            <p className="mt-2 text-lg font-semibold text-white">{summary.data?.analysis_runs ?? 0}</p>
          </Card>
          <Card>
            <p className="text-xs uppercase tracking-wide text-slate-500">Database</p>
            <div className="mt-2">
              <StatusPill status={health.data?.database ?? "unknown"} />
            </div>
          </Card>
        </div>

        <Card title="Repository registrations">
          {chartData.length === 0 ? (
            <p className="text-sm text-slate-400">
              Charts will appear after repositories are registered. This is registration activity only — not scan
              results.
            </p>
          ) : (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="day" stroke="#64748b" fontSize={12} />
                  <YAxis allowDecimals={false} stroke="#64748b" fontSize={12} />
                  <Tooltip
                    contentStyle={{ background: "#0f172a", border: "1px solid #1e293b", color: "#e2e8f0" }}
                  />
                  <Bar dataKey="count" fill="#22d3ee" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </Card>

        <Card title="Register a repository">
          <RepositoryForm onSubmit={register} submitting={submitting} />
        </Card>

        <Card title="Registered repositories">
          <RepositoryTable repositories={repos.data ?? []} />
        </Card>

        <Card title="Planned agents">
          <div className="grid gap-3 md:grid-cols-2">
            {(summary.data?.agents ?? []).map((agent) => (
              <div key={agent.id} className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <p className="font-medium text-slate-100">{agent.name}</p>
                  <StatusPill status={agent.status} />
                </div>
                <p className="mt-2 text-sm text-slate-400">{agent.description}</p>
              </div>
            ))}
          </div>
        </Card>

        <AgentEmptyPanel
          agentName="Analysis pipeline"
          capability="The command center can store repositories and report live API health."
        />
      </div>
    </AppShell>
  )
}
