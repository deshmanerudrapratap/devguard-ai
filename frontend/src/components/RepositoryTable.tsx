import type { Repository } from "../api/types"
import { Button } from "./ui/Button"
import { EmptyState } from "./ui/EmptyState"

type Props = {
  repositories: Repository[]
  onDelete?: (id: number) => void
  deletingId?: number | null
}

export function RepositoryTable({ repositories, onDelete, deletingId }: Props) {
  if (repositories.length === 0) {
    return (
      <EmptyState
        title="No repositories registered"
        description="Register a local path or remote URL to add it to the command center. No scans have been executed."
      />
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[640px] text-left text-sm">
        <thead className="text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="pb-3 font-medium">Name</th>
            <th className="pb-3 font-medium">Location</th>
            <th className="pb-3 font-medium">Registered</th>
            {onDelete ? <th className="pb-3 font-medium">Actions</th> : null}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {repositories.map((repo) => (
            <tr key={repo.id} className="align-top">
              <td className="py-3">
                <div className="font-medium text-slate-100">{repo.name}</div>
                {repo.description ? <div className="text-xs text-slate-500">{repo.description}</div> : null}
              </td>
              <td className="py-3 text-slate-400">
                <div>{repo.local_path ?? "—"}</div>
                <div className="text-xs text-slate-500">{repo.remote_url ?? "No remote URL"}</div>
              </td>
              <td className="py-3 text-slate-400">{new Date(repo.created_at).toLocaleString()}</td>
              {onDelete ? (
                <td className="py-3">
                  <Button
                    variant="danger"
                    type="button"
                    disabled={deletingId === repo.id}
                    onClick={() => onDelete(repo.id)}
                  >
                    {deletingId === repo.id ? "Removing…" : "Remove"}
                  </Button>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
