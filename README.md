# DevGuard AI

Autonomous Software Engineering Command Center. This repository is the **foundation stage**: a working React dashboard, FastAPI control plane, SQLite registry, and modular stubs for future agents.

No security scans, quality scores, or refactoring results are fabricated. Agent workspaces show honest empty states until those agents are implemented.

## Architecture

```
frontend (React + Vite + Tailwind + Recharts)
        REST /api
backend (FastAPI + SQLite)
agents / scanners / refactoring / prediction  <- contracts only
```

## Prerequisites

- Node.js 20+
- Python 3.11+

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

Health check:

```powershell
curl http://127.0.0.1:8000/api/health
```

## Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173

Vite proxies `/api` to the FastAPI server, so the dashboard talks to the real backend.

## Tests

From the repository root, with the backend virtualenv active:

```powershell
pip install -r backend/requirements.txt
pytest tests
```

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Process and SQLite connectivity |
| GET | `/api/repositories` | List registered repositories |
| POST | `/api/repositories` | Register a repository |
| GET | `/api/repositories/{id}` | Fetch one repository |
| PATCH | `/api/repositories/{id}` | Update location/description |
| DELETE | `/api/repositories/{id}` | Remove a repository |
| GET | `/api/dashboard/summary` | Counts, agent contracts, recent repos |

Register a repository:

```json
{
  "name": "demo-target",
  "local_path": "D:\\devguard-ai\\demo-target",
  "remote_url": null,
  "description": "Local sample workspace"
}
```

Provide `local_path`, `remote_url`, or both.

## Project layout

- `frontend/` command center UI
- `backend/` FastAPI app and SQLite models
- `agents/` BaseAgent plus unimplemented agent classes
- `scanners/` scanner interface
- `refactoring/` future guarded rewrite pipeline
- `prediction/` future forecasting pipeline
- `demo-target/` sample codebase you can register
- `tests/` API and stub tests
- `docs/` architecture notes
- `AGENTS.md` development rules for later agent work

## What this stage does not do

- It does not scan code.
- It does not invent vulnerabilities or quality scores.
- It does not run refactoring, prediction, orchestration, or rollback.
