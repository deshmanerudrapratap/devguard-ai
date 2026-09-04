import type { ReactNode } from "react"

type Props = {
  title?: string
  action?: ReactNode
  className?: string
  children: ReactNode
}

export function Card({ title, action, className = "", children }: Props) {
  return (
    <section className={`rounded-2xl border border-slate-800 bg-slate-950/70 p-5 shadow-xl shadow-black/20 ${className}`}>
      {(title || action) && (
        <div className="mb-4 flex items-start justify-between gap-4">
          {title ? <h2 className="text-sm font-semibold tracking-wide text-slate-200">{title}</h2> : <span />}
          {action}
        </div>
      )}
      {children}
    </section>
  )
}
