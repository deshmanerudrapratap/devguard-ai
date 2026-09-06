import { useState } from "react"
import { AppShell } from "../components/layout/AppShell"
import { api } from "../api/client"

export function CodeQualityPage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    quality_score?: number
    quality_status?: string
    total_findings?: number
    status?: string
  } | null>(null)

  const [error, setError] = useState<string | null>(null)

  async function runQualityAnalysis() {
    setLoading(true)
    setError(null)

    try {
      const response = await api.runAnalysis({
        repository_id: 1,
        repository_name: "demo-target",
        local_path: "demo-target",
      })

      const results = response.payload.results as Array<{
        agent_id: string
        status: string
        payload: {
          quality_score?: number
          quality_status?: string
          total_findings?: number
        }
      }>

      const qualityAgent = results.find(
        (agent) => agent.agent_id === "code-quality"
      )

      if (qualityAgent) {
        setResult({
          ...qualityAgent.payload,
          status: qualityAgent.status,
        })
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Code quality analysis failed"
      )
    } finally {
      setLoading(false)
    }
  }

  const qualityScore = result?.quality_score ?? 0
  const qualityStatus = result?.quality_status ?? "UNKNOWN"
  const findings = result?.total_findings ?? 0

  return (
    <AppShell
      title="Code Quality"
      subtitle="Maintainability and complexity analysis"
      health="ok"
    >
      <div className="space-y-7">

        {/* Header Card */}

        <div className="flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-950 p-7">
          <div>
            <h2 className="text-2xl font-bold text-white">
              Code Quality Agent
            </h2>

            <p className="mt-2 text-slate-400">
              Analyze code complexity, maintainability, and quality issues.
            </p>
          </div>

          <button
            onClick={() => void runQualityAnalysis()}
            disabled={loading}
            className="rounded-xl bg-cyan-500 px-7 py-4 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
          >
            {loading
              ? "Analyzing..."
              : "Run Quality Analysis"}
          </button>
        </div>

        {/* Error */}

        {error && (
          <div className="rounded-xl border border-red-800 bg-red-950/40 p-5 text-red-300">
            {error}
          </div>
        )}

        {/* Metrics */}

        {result && (
          <>
            <div className="grid gap-5 md:grid-cols-3">

              {/* Quality Score */}

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-sm uppercase text-slate-500">
                  Quality Score
                </p>

                <p className="mt-4 text-4xl font-bold text-white">
                  {qualityScore}
                </p>
              </div>

              {/* Quality Status */}

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-sm uppercase text-slate-500">
                  Quality Status
                </p>

                <p className="mt-4 text-3xl font-bold text-cyan-400">
                  {qualityStatus}
                </p>
              </div>

              {/* Findings */}

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-sm uppercase text-slate-500">
                  Findings
                </p>

                <p className="mt-4 text-4xl font-bold text-white">
                  {findings}
                </p>
              </div>

            </div>

            {/* Result */}

            <div className="rounded-2xl border border-slate-800 bg-slate-950 p-7">

              <h3 className="text-xl font-bold text-white">
                Code Quality Result
              </h3>

              <p className="mt-5 text-slate-400">
                Code quality analysis completed successfully.
              </p>

              <p className="mt-4 text-cyan-400">
                Agent Status: {result.status ?? "ready"}
              </p>

            </div>
          </>
        )}

      </div>
    </AppShell>
  )
}