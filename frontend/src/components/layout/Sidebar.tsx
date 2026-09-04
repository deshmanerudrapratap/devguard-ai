import { NavLink } from "react-router-dom"

const links = [
  { to: "/", label: "Overview" },
  { to: "/repositories", label: "Repository Intelligence" },
  { to: "/security", label: "Security" },
  { to: "/quality", label: "Code Quality" },
  { to: "/refactoring", label: "Refactoring" },
  { to: "/prediction", label: "Predictive Maintenance" },
  { to: "/operations", label: "Autonomous Operations" },
  { to: "/reports", label: "Reports" },
]

export function Sidebar() {
  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-slate-800 bg-[#050814]">
      <div className="border-b border-slate-800 px-5 py-5">
        <p className="text-[11px] font-semibold tracking-[0.22em] text-cyan-400">DEVGUARD AI</p>
        <h1 className="mt-1 text-lg font-semibold text-white">Command Center</h1>
        <p className="mt-1 text-xs text-slate-500">Autonomous software engineering</p>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={({ isActive }) =>
              `block rounded-lg px-3 py-2 text-sm transition ${
                isActive
                  ? "bg-cyan-500/10 text-cyan-200"
                  : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-slate-800 px-5 py-4 text-xs text-slate-500">
        Foundation stage · agents pending
      </div>
    </aside>
  )
}
