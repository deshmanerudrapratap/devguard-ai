export function SuccessBanner({ message }: { message: string }) {
  return (
    <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
      {message}
    </div>
  )
}
