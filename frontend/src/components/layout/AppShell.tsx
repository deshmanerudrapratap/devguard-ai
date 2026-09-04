import type { ReactNode } from "react"
import { Sidebar } from "./Sidebar"
import { TopBar } from "./TopBar"

type Props = {
  title: string
  subtitle: string
  health?: string
  children: ReactNode
}

export function AppShell({ title, subtitle, health, children }: Props) {
  return (
    <div className="flex min-h-screen bg-[#070b14] text-slate-200">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar title={title} subtitle={subtitle} health={health} />
        <main className="flex-1 overflow-y-auto px-8 py-6">{children}</main>
      </div>
    </div>
  )
}
