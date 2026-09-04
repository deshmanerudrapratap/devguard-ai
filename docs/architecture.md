# Architecture

DevGuard AI is split into a React command center, a FastAPI control plane, a SQLite
system of record, and isolated packages for future agents and scanners.

```
frontend  ->  REST /api/*  ->  backend/app
                                 ├── models / schemas / routers / services
                                 └── later: agents, scanners, refactoring, prediction
```

# API foundation

- `GET /api/health`
- `GET|POST /api/repositories`
- `GET|PATCH|DELETE /api/repositories/{id}`
- `GET /api/dashboard/summary`

# Agent roadmap

Planned packages under `agents/` are stubs only. Do not invent scan results.
