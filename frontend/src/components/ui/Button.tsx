import type { ButtonHTMLAttributes, ReactNode } from "react"

type Variant = "primary" | "secondary" | "danger" | "ghost"

const styles: Record<Variant, string> = {
  primary:
    "bg-cyan-500 text-slate-950 hover:bg-cyan-400 disabled:bg-cyan-500/40 disabled:text-slate-700",
  secondary:
    "border border-slate-700 bg-slate-900 text-slate-200 hover:border-slate-500 hover:bg-slate-800",
  danger: "bg-rose-500/15 text-rose-300 hover:bg-rose-500/25 border border-rose-500/30",
  ghost: "text-slate-300 hover:bg-slate-800/80",
}

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant
  children: ReactNode
}

export function Button({ variant = "primary", className = "", children, ...props }: Props) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-lg px-3.5 py-2 text-sm font-medium transition disabled:cursor-not-allowed ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
