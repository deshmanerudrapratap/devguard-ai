import type { ReactNode } from "react"

type Props = {
  title: string
  description: string
  action?: ReactNode
}

export function EmptyState({ title, description, action }: Props) {
  return (
    <div className="rounded-xl border border-dashed border-slate-700 bg-slate-900/40 px-5 py-8 text-center">
      <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">{description}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  )
}
