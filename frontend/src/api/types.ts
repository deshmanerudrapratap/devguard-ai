export type AgentStatusValue = "not_implemented" | "ready" | "running" | "failed"

export type HealthResponse = {
  status: string
  service: string
  version: string
  database: string
}

export type Repository = {
  id: number
  name: string
  local_path: string | null
  remote_url: string | null
  description: string | null
  created_at: string
  updated_at: string
}

export type RepositoryPayload = {
  name: string
  local_path?: string
  remote_url?: string
  description?: string
}

export type AgentStatus = {
  id: string
  name: string
  status: AgentStatusValue
  description: string
}

export type DashboardSummary = {
  service: string
  version: string
  system_status: string
  repository_count: number
  analysis_runs: number
  agents: AgentStatus[]
  recent_repositories: Repository[]
  notice: string
}

export type ApiError = {
  error: {
    code: string
    message: string
    details?: unknown
  }
}
