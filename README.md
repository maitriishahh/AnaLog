# AnaLog — Log File Intelligence Engine

## Problem Statement

Servers generate large amounts of log data whenever users log in, access pages,
make payments, or encounter errors. Manually analyzing these logs makes it
difficult to identify unusual activity, frequently failing endpoints, or
problematic users.

## Solution

AnaLog is a **Log File Intelligence Engine** that takes raw server logs,
parses and organizes them, and automatically analyzes the data to identify
patterns such as:

- the most active users
- the most frequently accessed endpoints
- error-heavy (frequently failing) endpoints
- overall and per-user error rates
- users exhibiting suspicious activity

Finally, it generates a summary report that gives a quick overview of the
server's activity and potential issues.

### In simple terms

```
Raw server logs  →  Process & analyze  →  Detect patterns / problems  →  Generate useful report
```

---

## Project Status

- **V1 (current):** Static, hand-written dummy logs (`logs.py`) are parsed and
  analyzed in `main.py`, which prints a plain-text report to the console.
  No database, no web server, no real traffic.
- **V2 (in progress):** Re-architect into a documented, testable service that
  ingests **real HTTP logs**, stores them in **SQLite** (via SQLAlchemy),
  exposes **REST endpoints** and **reports**, is verified with **real traffic
  tests**, and is instrumented with **OpenTelemetry**.

> This repository currently contains only the **scaffold** (folder structure +
> this document). No V2 logic has been implemented yet — each phase below will
> land code together with its documentation updates.

---

## Architecture Overview (Target)

```
                 ┌─────────────────────────────────────────────┐
                 │                AnaLog V2                     │
                 │                                               │
   Real HTTP     │   ┌──────────┐    ┌────────────┐             │
   logs ─────────┼──▶│ ingestion│───▶│   SQLite   │             │
   (Phase 2)     │   │(analytics│    │ (SQLAlchemy│             │
                 │   │ /ingest) │    │  Phase 4)  │             │
                 │   └──────────┘    └─────┬──────┘             │
                 │         │               │                    │
                 │         ▼               ▼                    │
                 │   ┌────────────┐   ┌───────────┐             │
                 │   │ analytics/ │   │   REST    │             │
                 │   │  analyze   │◀──│  endpoints│             │
                 │   └─────┬──────┘   │(api/routes)│            │
                 │         │          └─────┬─────┘             │
                 │         ▼                ▼                    │
                 │   ┌────────────┐   ┌───────────┐             │
                 │   │  reports/  │   │  FastAPI   │            │
                 │   │  report    │   │  (app.py)  │            │
                 │   └────────────┘   └───────────┘             │
                 │         │                                     │
                 │         ▼                                     │
                 │   Summary report (JSON / text)                │
                 │                                               │
                 │   ── OpenTelemetry tracing across pipeline ── │
                 └─────────────────────────────────────────────┘
```

---

## Directory Layout

| Path                | Responsibility (target)                                              |
|---------------------|----------------------------------------------------------------------|
| `app.py`            | FastAPI application entrypoint (run with `uvicorn app:app`).         |
| `api/`              | HTTP layer — REST endpoints that expose analytics and reports.       |
| `api/routes.py`     | Route definitions (`/api/stats`, `/api/users`, `/api/report`, ...).  |
| `db/`               | Persistence layer using SQLAlchemy.                                  |
| `db/session.py`     | Engine, `SessionLocal`, and `init_db()` helper.                      |
| `db/models.py`      | ORM models (e.g. `Log`: timestamp, severity, user, endpoint, raw).   |
| `analytics/`        | Core intelligence: parsing, analysis, and ingestion.                 |
| `analytics/parse.py`| Parse raw log lines into structured records.                         |
| `analytics/analyze.py`| Compute metrics (totals, severity %, active users, suspicious).   |
| `analytics/ingest.py`| Ingest real HTTP logs into the storage layer.                      |
| `reports/`          | Generate the final human-readable / machine-readable summary report. |
| `reports/report.py` | Build report from analytics output (dict → JSON / text).            |
| `tests/`            | `pytest` suite (parsing, analytics, API, real-traffic integration). |
| `data/`             | Local SQLite database storage (`analog.db`, git-ignored).            |
| `logs.py`           | **V1 sample data** — static dummy log lines (kept for reference).    |
| `main.py`           | **V1 CLI** — prints the analysis report (kept for reference).        |

---

## Build Progression (V2 Roadmap)

Each phase is implemented together with its documentation updates so the repo
never becomes a bare code dump.

1. **Refactor current code** — Port `main.py` logic into the `analytics/`
   package as pure, testable functions; route report output through
   `reports/report.py`. Seed the README/architecture docs.
2. **FastAPI test server** — Stand up `app.py` with a `/health` endpoint and a
   `/report` endpoint returning JSON.
3. **Real HTTP logs** — Emit genuine access-log lines from server traffic
   (plus a helper to simulate users/endpoints).
4. **Log ingestion** — `analytics/ingest.py` normalizes raw logs into records.
5. **SQLite (SQLAlchemy)** — Persist logs via `db/models.py` + `db/session.py`;
   ingestion writes, analytics reads.
6. **AnaLog analytics** — Re-point `analytics/analyze.py` at SQLite; keep all V1
   metrics.
7. **REST endpoints + Reports** — `api/routes.py` exposes stats/users/endpoints/
   suspicious/report; `reports/` renders them.
8. **Real traffic tests** — `pytest` + FastAPI `TestClient` covering parsing,
   analytics, and API behavior under generated traffic.
9. **OpenTelemetry** — Instrument the pipeline with traces (see `docs/`
   when that phase lands).

---

## Setup

Requirements: **Python ≥ 3.13** and [`uv`](https://docs.astral.sh/uv/).

```bash
# Create / sync the virtual environment and dependencies
uv sync

# Activate the environment (optional; uv run prefixes commands otherwise)
source .venv/Scripts/activate   # Windows (PowerShell)
# source .venv/bin/activate     # macOS / Linux

# Run the V1 reference report (no server required)
python main.py
```

> V2 run/serve/test commands will be documented here as each phase is built.

---

## Notes

- `logs.py` and `main.py` are preserved from V1 as sample data and a CLI
  reference; they are not part of the V2 service.
- `data/` and the virtual environment are git-ignored (see `.gitignore`).
