import { Badge } from "./Badge"

type Props = {
  status: string
}

export function StatusPill({ status }: Props) {
  if (status === "ok" || status === "operational" || status === "connected" || status === "ready") {
    return <Badge tone="success">{status}</Badge>
  }
  if (status === "not_implemented") {
    return <Badge tone="warning">not implemented</Badge>
  }
  if (status === "error" || status === "failed" || status === "degraded" || status === "disconnected") {
    return <Badge tone="danger">{status}</Badge>
  }
  return <Badge tone="info">{status}</Badge>
}
