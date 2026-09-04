import { StatusPill } from "../ui/StatusPill"

type Props = {
  title: string
  subtitle: string
  health?: string
}

export function TopBar({ title, subtitle, health }: Props) {
  return (
    <header className="flex items-center justify-between border-b border-slate-800 px-8 py-5">
      <div>
        <h2 className="text-xl font-semibold text-white">{title}</h2>
        <p className="mt-1 text-sm text-slate-400">{subtitle}</p>
      </div>
      <div className="flex items-center gap-3 text-xs text-slate-400">
        <span>API health</span>
        <StatusPill status={health ?? "unknown"} />
      </div>
    </header>
  )
}
