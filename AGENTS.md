# DevGuard AI — agent architecture

This file is the contract for humans and coding agents working in this repository.

## Product

DevGuard AI is an Autonomous Software Engineering Command Center. The foundation already provides:

- a React command center
- a FastAPI control plane
- SQLite persistence for registered repositories
- REST endpoints for health, repositories, and dashboard summary

Later stages plug real agents into this control plane. Do not collapse agents into the UI or invent analysis results.

## Layout

| Path | Role |
| --- | --- |
| `frontend/` | Dashboard only. Talks to `/api`. No business logic that belongs on the server. |
| `backend/app` | HTTP, persistence, validation, error envelopes. |
| `agents/` | One module per agent. Implement `BaseAgent.run`. |
| `scanners/` | Tool adapters used by agents. Return structured findings or an unimplemented result. |
| `refactoring/` | Guarded rewrite planning and application. |
| `prediction/` | Forecasting models. |
| `demo-target/` | Sample workspace for later real scans. |
| `tests/` | API and contract tests. Add tests when an agent starts returning real data. |

## Planned agents

These exist as stubs with `status = not_implemented`:

- Security Agent
- Repository Intelligence Agent
- Code Quality Agent
- Dependency Agent
- Refactoring Agent
- Predictive Maintenance Agent
- Autonomous Orchestrator
- Validation / Test Agent
- Rollback system
- Reporting Agent

Do not mark them ready until they produce real, reproducible output.

## Development rules

1. Keep the architecture modular. New capabilities belong in `agents/`, `scanners/`, `refactoring/`, or `prediction/`, then get a thin FastAPI router.
2. Never fake scan results, scores, diffs, or reports in the UI or API.
3. Empty states must say the agent is not implemented, not that the repo is clean.
4. Persist durable artifacts in SQLite (or a later database). Do not keep source of truth in React state.
5. Preserve loading, error, and success states for every new user-facing action.
6. CORS is configured for local Vite. Extend `DEVGUARD_` settings instead of hardcoding secrets.
7. Do not overwrite unrelated files. Prefer additive changes.
8. Validation and rollback must wrap any future write to a registered repository.
9. Public API errors use `{ "error": { "code", "message" } }`.
10. Charts may visualize real operational data (repository registrations, job status). They must not display synthetic vulnerabilities.

## API conventions

- Prefix: `/api`
- Health: `GET /api/health`
- Repositories: `/api/repositories`
- Dashboard: `GET /api/dashboard/summary`

Future agent routes should follow `/api/agents/{agent_id}/...` and accept a `repository_id`.

## Frontend conventions

- Reuse `AppShell`, `Card`, `EmptyState`, `LoadingState`, `ErrorBanner`, `SuccessBanner`, and `StatusPill`.
- Fetch through `src/api/client.ts`.
- Navigation sections are fixed: Overview, Repository Intelligence, Security, Code Quality, Refactoring, Predictive Maintenance, Autonomous Operations, Reports.

## Backend conventions

- SQLAlchemy models in `backend/app/models`
- Pydantic schemas in `backend/app/schemas`
- Route handlers stay thin; logic lives in `services/`
- SQLite file is created under `backend/data/` and is gitignored
