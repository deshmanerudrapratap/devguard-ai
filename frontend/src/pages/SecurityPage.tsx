import { useEffect, useState } from "react"
import { api } from "../api/client"
import type { Repository } from "../api/types"
import { AppShell } from "../components/layout/AppShell"

type AgentResult = {
  agent_id: string
  status: string
  message: string
  payload: Record<string, unknown>
}

export function SecurityPage() {
  const [repositories, setRepositories] = useState<Repository[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AgentResult | null>(null)

  useEffect(() => {
    async function loadRepositories() {
      try {
        const data = await api.listRepositories()
        setRepositories(data)
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

  async function runSecurityScan() {
    const repository = repositories[0]

    if (!repository) {
      setError("No repository available.")
      return
    }

    try {
      setRunning(true)
      setError(null)

      const response = await api.runAnalysis({
        repository_id: repository.id,
        repository_name: repository.name,
        local_path: repository.local_path,
      })

      const data = response.payload as {
        results?: AgentResult[]
      }

      const securityResult = data.results?.find(
        (agent) => agent.agent_id === "security-scanner"
      )

      setResult(securityResult ?? null)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Security scan failed"
      )
    } finally {
      setRunning(false)
    }
  }

  const findings =
    (result?.payload.total_findings as number) ?? 0

  const securityStatus =
    (result?.payload.security_status as string) ?? "UNKNOWN"

  const riskScore =
    (result?.payload.risk_score as number) ?? 0

  return (
    <AppShell
      title="Security"
      subtitle="Vulnerability and secret analysis"
      health="ok"
    >
      <div className="space-y-6">

        <div className="rounded-xl border border-slate-800 bg-slate-950 p-6">
          <div className="flex flex-wrap items-center justify-between gap-4">

            <div>
              <h2 className="text-xl font-bold text-white">
                Security Agent
              </h2>

              <p className="mt-2 text-sm text-slate-400">
                Scan repositories for vulnerabilities, secrets, and insecure patterns.
              </p>
            </div>

            <button
              onClick={() => void runSecurityScan()}
              disabled={running || loading || repositories.length === 0}
              className="rounded-lg bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
            >
              {running ? "Scanning..." : "Run Security Scan"}
            </button>

          </div>
        </div>

        {loading && (
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-6 text-slate-400">
            Loading repository...
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-800 bg-red-950/40 p-5 text-red-300">
            {error}
          </div>
        )}

        {result && (
          <>

            <div className="grid gap-4 md:grid-cols-3">

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
                <p className="text-xs uppercase text-slate-500">
                  Findings
                </p>

                <p className="mt-3 text-3xl font-bold text-white">
                  {findings}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
                <p className="text-xs uppercase text-slate-500">
                  Security Status
                </p>

                <p className="mt-3 text-2xl font-bold text-cyan-400">
                  {securityStatus}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
                <p className="text-xs uppercase text-slate-500">
                  Risk Score
                </p>

                <p className="mt-3 text-3xl font-bold text-white">
                  {riskScore}
                </p>
              </div>

            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950 p-6">

              <h3 className="text-lg font-semibold text-white">
                Security Scan Result
              </h3>

              <p className="mt-3 text-slate-400">
                {result.message}
              </p>

              <p className="mt-3 text-sm text-cyan-400">
                Agent Status: {result.status}
              </p>

            </div>

          </>
        )}

      </div>
    </AppShell>
  )
}