import type {
  DashboardSummary,
  HealthResponse,
  Repository,
  RepositoryPayload,
} from "./types"

const API_BASE = "/api"

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {}),
      },
      ...init,
    })
  } catch {
    throw new Error("Unable to reach the DevGuard API. Confirm the backend is running on port 8000.")
  }

  if (response.status === 204) {
    return undefined as T
  }

  const data: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    const message =
      data && typeof data === "object" && "error" in data
        ? String((data as { error?: { message?: string } }).error?.message)
        : `Request failed with status ${response.status}`
    throw new Error(message || `Request failed with status ${response.status}`)
  }

  return data as T
}

export const api = {
  health: () => request<HealthResponse>("/health"),
  dashboardSummary: () => request<DashboardSummary>("/dashboard/summary"),
  listRepositories: () => request<Repository[]>("/repositories"),
  createRepository: (payload: RepositoryPayload) =>
    request<Repository>("/repositories", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  deleteRepository: (id: number) =>
  request<void>(`/repositories/${id}`, {
    method: "DELETE",
  }),

runAnalysis: (payload: {
  repository_id: number
  repository_name: string
  local_path: string
}) =>
  request<{
    status: string
    message: string
    payload: Record<string, unknown>
  }>("/analysis/run", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
}
