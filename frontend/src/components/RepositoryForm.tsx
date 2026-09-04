import { useState, type FormEvent } from "react"
import { Button } from "./ui/Button"

type Props = {
  onSubmit: (payload: {
    name: string
    local_path?: string
    remote_url?: string
    description?: string
  }) => Promise<void>
  submitting: boolean
}

export function RepositoryForm({ onSubmit, submitting }: Props) {
  const [name, setName] = useState("")
  const [localPath, setLocalPath] = useState("")
  const [remoteUrl, setRemoteUrl] = useState("")
  const [description, setDescription] = useState("")
  const [formError, setFormError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!name.trim()) {
      setFormError("Repository name is required.")
      return
    }
    if (!localPath.trim() && !remoteUrl.trim()) {
      setFormError("Provide a local path, a remote URL, or both.")
      return
    }
    setFormError(null)
    await onSubmit({
      name: name.trim(),
      local_path: localPath.trim() || undefined,
      remote_url: remoteUrl.trim() || undefined,
      description: description.trim() || undefined,
    })
    setName("")
    setLocalPath("")
    setRemoteUrl("")
    setDescription("")
  }

  return (
    <form onSubmit={handleSubmit} className="grid gap-3 md:grid-cols-2">
      <label className="grid gap-1 text-xs text-slate-400">
        Name
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
          placeholder="payments-service"
        />
      </label>
      <label className="grid gap-1 text-xs text-slate-400">
        Local path
        <input
          value={localPath}
          onChange={(event) => setLocalPath(event.target.value)}
          className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
          placeholder="D:\\devguard-ai\\demo-target"
        />
      </label>
      <label className="grid gap-1 text-xs text-slate-400">
        Remote URL
        <input
          value={remoteUrl}
          onChange={(event) => setRemoteUrl(event.target.value)}
          className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
          placeholder="https://github.com/org/repo.git"
        />
      </label>
      <label className="grid gap-1 text-xs text-slate-400">
        Description
        <input
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500"
          placeholder="Optional notes"
        />
      </label>
      {formError ? <p className="text-sm text-rose-300 md:col-span-2">{formError}</p> : null}
      <div className="md:col-span-2">
        <Button type="submit" disabled={submitting}>
          {submitting ? "Registering…" : "Register repository"}
        </Button>
      </div>
    </form>
  )
}
