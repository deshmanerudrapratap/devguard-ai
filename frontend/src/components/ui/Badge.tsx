type Tone = "neutral" | "success" | "warning" | "danger" | "info"

const tones: Record<Tone, string> = {
  neutral: "bg-slate-800 text-slate-300",
  success: "bg-emerald-500/15 text-emerald-300",
  warning: "bg-amber-500/15 text-amber-300",
  danger: "bg-rose-500/15 text-rose-300",
  info: "bg-cyan-500/15 text-cyan-300",
}

export function Badge({ children, tone = "neutral" }: { children: string; tone?: Tone }) {
  return (
    <span className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${tones[tone]}`}>
      {children}
    </span>
  )
}
