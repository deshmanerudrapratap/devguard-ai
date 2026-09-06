import { useEffect, useState } from "react"
import type { Repository } from "../api/types"
import { AnalysisPanel } from "../components/AnalysisPanel"
import { AppShell } from "../components/layout/AppShell"

export function OverviewPage() {
  const [repositories, setRepositories] = useState<Repository[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadRepositories() {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch("/api/repositories")

        if (!response.ok) {
          throw new Error(
            `Failed to load repositories: ${response.status}`
          )
        }

        const data = await response.json()

        const repositoryList = Array.isArray(data)
          ? data
          : Array.isArray(data.payload)
            ? data.payload
            : []

        setRepositories(repositoryList)
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load repositories"
        )
      } finally {
        setLoading(false)
      }
    }

    void loadRepositories()
  }, [])

  const selectedRepository = repositories[0]

  return (
    <AppShell
      title="Overview"
      subtitle="Operational status of the DevGuard AI command center"
      health="ok"
    >
      <div className="space-y-6">

        {loading && (
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-6 text-slate-400">
            Loading repositories...
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-800 bg-red-950/40 p-5 text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && !selectedRepository && (
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-8">
            <h2 className="text-xl font-semibold text-white">
              No repository selected
            </h2>

            <p className="mt-2 text-slate-400">
              Go to Repository Intelligence and register a repository.
            </p>
          </div>
        )}

        {!loading && selectedRepository && (
          <AnalysisPanel repository={selectedRepository} />
        )}

        <div className="grid gap-4 md:grid-cols-4">

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Service
            </p>

            <p className="mt-3 text-xl font-bold text-white">
              DevGuard AI
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Repositories
            </p>

            <p className="mt-3 text-2xl font-bold text-white">
              {repositories.length}
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Autonomous Agents
            </p>

            <p className="mt-3 text-2xl font-bold text-cyan-400">
              6
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
            <p className="text-xs uppercase tracking-wide text-slate-500">
              Database
            </p>

            <p className="mt-3 inline-block rounded-full bg-emerald-950 px-3 py-1 text-sm font-semibold text-emerald-400">
              connected
            </p>
          </div>

        </div>

      </div>
    </AppShell>
  )
}