import { useState } from "react"
import { api } from "../api/client"
import type { Repository } from "../api/types"
import { Card } from "./ui/Card"

type Props = {
  repository: Repository | undefined
}

type AgentResult = {
  agent_id: string
  status: string
  message: string
  payload: Record<string, unknown>
}

function getAgent(
  results: AgentResult[],
  agentId: string
): AgentResult | undefined {
  return results.find((agent) => agent.agent_id === agentId)
}

export function AnalysisPanel({ repository }: Props) {
  const [running, setRunning] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function run() {
    if (!repository?.local_path) {
      setError("Repository path is missing.")
      return
    }

    setRunning(true)
    setError(null)

    try {
      const response = await api.runAnalysis({
        repository_id: repository.id,
        repository_name: repository.name,
        local_path: repository.local_path,
      })

      setResult(response.payload)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed")
    } finally {
      setRunning(false)
    }
  }

  const results = (result?.results ?? []) as AgentResult[]

  const repositoryAgent = getAgent(
    results,
    "repository-intelligence"
  )

  const securityAgent = getAgent(
    results,
    "security-scanner"
  )

  const qualityAgent = getAgent(
    results,
    "code-quality"
  )

  const maintenanceAgent = getAgent(
    results,
    "predictive-maintenance"
  )

  const repositoryData = repositoryAgent?.payload
  const securityData = securityAgent?.payload
  const qualityData = qualityAgent?.payload
  const maintenanceData = maintenanceAgent?.payload

  const securityFindings =
    (securityData?.total_findings as number) ?? 0

  const securityRisk =
    (securityData?.security_status as string) ?? "UNKNOWN"

  const securityScore =
    (securityData?.risk_score as number) ?? 0

  const qualityScore =
    (qualityData?.quality_score as number) ?? 0

  const qualityStatus =
    (qualityData?.quality_status as string) ?? "UNKNOWN"

  const qualityFindings =
    (qualityData?.total_findings as number) ?? 0

  const totalFiles =
    (maintenanceData?.metrics as Record<string, unknown>)
      ?.total_files as number ?? 0

  const sourceFiles =
    (maintenanceData?.metrics as Record<string, unknown>)
      ?.source_files as number ?? 0

  const totalLines =
    (maintenanceData?.metrics as Record<string, unknown>)
      ?.total_lines as number ?? 0

  const maintenanceRisk =
    (maintenanceData?.maintenance_risk as Record<string, unknown>)
      ?.level as string ?? "UNKNOWN"

  const maintenanceScore =
    (maintenanceData?.maintenance_risk as Record<string, unknown>)
      ?.score as number ?? 0

  return (
    <Card title="Autonomous Analysis">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-lg font-semibold text-white">
            {repository?.name ?? "No repository"}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            Multi-agent autonomous software engineering analysis.
          </p>
        </div>

        <button
          onClick={() => void run()}
          disabled={running || !repository}
          className="rounded-lg bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50"
        >
          {running ? "Analyzing..." : "Run Autonomous Analysis"}
        </button>
      </div>

      {error && (
        <div className="mt-5 rounded-lg border border-red-800 bg-red-950/40 p-4 text-sm text-red-300">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 space-y-6">

          <div>
            <h3 className="mb-3 text-sm font-semibold text-cyan-400">
              🤖 Agent Pipeline
            </h3>

            <div className="grid gap-3 md:grid-cols-4">
              {results.map((agent) => (
                <div
                  key={agent.agent_id}
                  className="rounded-xl border border-slate-800 bg-slate-900 p-4"
                >
                  <p className="text-sm font-semibold text-white">
                    {agent.agent_id}
                  </p>

                  <p className="mt-2 text-xs text-cyan-400">
                    {agent.status}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="mb-3 text-sm font-semibold text-cyan-400">
              🛡️ Security Analysis
            </h3>

            <div className="grid gap-4 md:grid-cols-3">

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Findings
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {securityFindings}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Security Status
                </p>

                <p className="mt-2 text-xl font-bold text-cyan-400">
                  {securityRisk}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Risk Score
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {securityScore}
                </p>
              </div>

            </div>
          </div>

          <div>
            <h3 className="mb-3 text-sm font-semibold text-cyan-400">
              📊 Code Quality
            </h3>

            <div className="grid gap-4 md:grid-cols-3">

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Quality Score
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {qualityScore}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Quality Status
                </p>

                <p className="mt-2 text-xl font-bold text-cyan-400">
                  {qualityStatus}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Findings
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {qualityFindings}
                </p>
              </div>

            </div>
          </div>

          <div>
            <h3 className="mb-3 text-sm font-semibold text-cyan-400">
              🔮 Predictive Maintenance
            </h3>

            <div className="grid gap-4 md:grid-cols-4">

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Files
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {totalFiles}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Source Files
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {sourceFiles}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Lines
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  {totalLines}
                </p>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
                <p className="text-xs uppercase text-slate-500">
                  Maintenance Risk
                </p>

                <p className="mt-2 text-xl font-bold text-cyan-400">
                  {maintenanceRisk}
                </p>

                <p className="text-xs text-slate-500">
                  Score: {maintenanceScore}
                </p>
              </div>

            </div>
          </div>

        </div>
      )}
    </Card>
  )
}