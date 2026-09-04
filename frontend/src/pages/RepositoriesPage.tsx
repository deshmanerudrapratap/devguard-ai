import { useState } from "react"
import { api } from "../api/client"
import type { RepositoryPayload } from "../api/types"
import { AgentEmptyPanel } from "../components/AgentEmptyPanel"
import { AppShell } from "../components/layout/AppShell"
import { RepositoryForm } from "../components/RepositoryForm"
import { RepositoryTable } from "../components/RepositoryTable"
import { Card } from "../components/ui/Card"
import { ErrorBanner } from "../components/ui/ErrorBanner"
import { LoadingState } from "../components/ui/LoadingState"
import { SuccessBanner } from "../components/ui/SuccessBanner"
import { useAsync } from "../hooks/useAsync"

export function RepositoriesPage() {
  const health = useAsync(() => api.health(), [])
  const repos = useAsync(() => api.listRepositories(), [])
  const [submitting, setSubmitting] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)

  async function register(payload: RepositoryPayload) {
    setSubmitting(true)
    setActionError(null)
    setSuccess(null)
    try {
      const created = await api.createRepository(payload)
      setSuccess(`Stored ${created.name} in SQLite. Intelligence mapping has not run.`)
      await repos.reload()
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "Registration failed")
    } finally {
      setSubmitting(false)
    }
  }

  async function remove(id: number) {
    setDeletingId(id)
    setActionError(null)
    setSuccess(null)
    try {
      await api.deleteRepository(id)
      setSuccess("Repository removed from the registry.")
      await repos.reload()
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "Delete failed")
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <AppShell
      title="Repository Intelligence"
      subtitle="Registry of engineering workspaces. Architecture mapping is not implemented yet."
      health={health.data?.status}
    >
      <div className="grid gap-5">
        {repos.loading ? <LoadingState label="Loading registered repositories…" /> : null}
        {repos.error ? <ErrorBanner message={repos.error} onRetry={() => void repos.reload()} /> : null}
        {actionError ? <ErrorBanner message={actionError} /> : null}
        {success ? <SuccessBanner message={success} /> : null}

        <Card title="Register repository">
          <RepositoryForm onSubmit={register} submitting={submitting} />
        </Card>

        <Card title="Workspace registry">
          <RepositoryTable
            repositories={repos.data ?? []}
            onDelete={(id) => void remove(id)}
            deletingId={deletingId}
          />
        </Card>

        <AgentEmptyPanel
          agentName="Repository Intelligence Agent"
          capability="This section will later show architecture maps, ownership, and change hotspots."
        />
      </div>
    </AppShell>
  )
}
