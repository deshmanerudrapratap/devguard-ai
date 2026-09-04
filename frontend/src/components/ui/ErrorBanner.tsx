type Props = {
  message: string
  onRetry?: () => void
}

export function ErrorBanner({ message, onRetry }: Props) {
  return (
    <div className="flex items-start justify-between gap-4 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
      <p>{message}</p>
      {onRetry ? (
        <button type="button" onClick={onRetry} className="shrink-0 font-medium text-rose-100 underline">
          Retry
        </button>
      ) : null}
    </div>
  )
}
