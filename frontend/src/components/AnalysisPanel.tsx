import { useState } from "react"
import { api } from "../api/client"
import type { Repository } from "../api/types"
import { Card } from "./ui/Card"

type Props = {
  repository: Repository | undefined
}

function findValue(data: unknown, key: string): unknown {
  if (!data || typeof data !== "object") return undefined

  const object = data as Record<string, unknown>

  if (key in object) return object[key]

  for (const value of Object.values(object)) {
    const found = findValue(value, key)
    if (found !== undefined) return found
  }

  return undefined
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

  const totalFiles = findValue(result, "total_files") as number | undefined
  const sourceFiles = findValue(result, "source_files") as number | undefined
  const totalLines = findValue(result, "total_lines") as number | undefined
  const riskLevel = findValue(result, "level") as string | undefined
  const riskScore = findValue(result, "score") as number | undefined

  return (
    <Card title="Autonomous Analysis">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-lg font-semibold text-white">
            {repository?.name ?? "No repository"}
          </p>

          <p className="mt-1 text-sm text-slate-400">
            Run the autonomous engineering analysis pipeline.
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
        <div className="mt-6 grid gap-4 md:grid-cols-4">
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase text-slate-500">Files</p>
            <p className="mt-2 text-2xl font-bold text-white">
              {totalFiles ?? 0}
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase text-slate-500">Source Files</p>
            <p className="mt-2 text-2xl font-bold text-white">
              {sourceFiles ?? 0}
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase text-slate-500">Lines</p>
            <p className="mt-2 text-2xl font-bold text-white">
              {totalLines ?? 0}
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <p className="text-xs uppercase text-slate-500">
              Maintenance Risk
            </p>
            <p className="mt-2 text-2xl font-bold text-cyan-400">
              {riskLevel ?? "UNKNOWN"}
            </p>
            <p className="text-xs text-slate-500">
              Score: {riskScore ?? 0}
            </p>
          </div>
        </div>
      )}
    </Card>
  )
}