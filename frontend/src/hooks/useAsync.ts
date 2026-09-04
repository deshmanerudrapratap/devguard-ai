import { useCallback, useEffect, useState } from "react"

type AsyncState<T> = {
  data: T | null
  loading: boolean
  error: string | null
}

export function useAsync<T>(loader: () => Promise<T>, deps: unknown[] = []) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: true,
    error: null,
  })

  const reload = useCallback(async () => {
    setState((current) => ({ ...current, loading: true, error: null }))
    try {
      const data = await loader()
      setState({ data, loading: false, error: null })
    } catch (error) {
      setState({
        data: null,
        loading: false,
        error: error instanceof Error ? error.message : "Unexpected error",
      })
    }
  }, deps)

  useEffect(() => {
    void reload()
  }, [reload])

  return { ...state, reload }
}
