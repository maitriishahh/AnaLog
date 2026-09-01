# AnaLog Changelog

Running log of changes to the codebase as V2 is built, one phase at a time.
Each phase lands code together with its documentation updates so the repo
never becomes a bare code dump.

---

## Phase 0 — Project scaffold & documentation foundation ✅

**Goal:** Establish the flat-with-folders structure and seed the
architecture/setup documentation. **No V2 logic implemented.**

### Added
- Folder skeleton: `api/`, `db/`, `analytics/`, `reports/`, `tests/`, `data/`
- Empty placeholder modules (no logic):
  - `app.py`
  - `api/__init__.py`, `api/routes.py`
  - `db/__init__.py`, `db/session.py`, `db/models.py`
  - `analytics/__init__.py`, `analytics/parse.py`, `analytics/analyze.py`, `analytics/ingest.py`
  - `reports/__init__.py`, `reports/report.py`
  - `tests/.gitkeep`, `data/.gitkeep`
- `.gitignore` — ignores `.venv/`, `__pycache__/`, `.idea/`, `data/*.db`
- `README.md` — problem statement, solution, target architecture diagram,
  directory layout table, V1→V2 status, 9-phase build roadmap, and setup

### Preserved (V1 reference, unchanged)
- `logs.py` — static dummy sample logs
- `main.py` — V1 CLI that prints the analysis report

---

## Phase 1 — Refactor current code ✅

**Goal:** Port `main.py` logic into the `analytics/` package as importable
functions; make `reports/report.py` return a structured dict instead of
printing to console.

### Added
- `analytics/parse.py` — `parse_logs()` extracted from `main.py`
- `analytics/analyze.py` — all analysis functions ported (totals, severity,
  active users, endpoints, suspicious activity); imports `parse_logs` from
  `analytics.parse`
- `reports/report.py` — `generate_report()` returns a dict with keys
  `total_requests`, `unique_users`, `unique_endpoints`, `severity`, `users`,
  `endpoints`, `suspicious_users` (console prints commented out)

### Notes
- `logs.py` remains the data source (still static dummy data at this point)
- `main.py` left untouched as V1 reference

---

## Phase 2 — FastAPI test server ✅

**Goal:** Create a FastAPI app with health check, report endpoint, and
sample routes; log real requests to `logs.jsonl`.

### Added
- `app.py` — FastAPI application with:
  - HTTP middleware that logs every request to `logs.jsonl` (timestamp,
    level, user_id, method, endpoint, status_code, response_time)
  - `GET /health` → `{"status": "healthy"}`
  - `GET /report` → returns `generate_report()` as JSON
  - `GET /login`, `GET /products`, `GET /payment` — sample routes for
    traffic generation
- `pyproject.toml` — added `fastapi>=0.141.1` dependency

---

## Phase 3 — Real HTTP logs ✅

**Goal:** Emit genuine access-log lines from real server traffic.

### Done
- The Phase 2 middleware already logs every HTTP request to `logs.jsonl`
  with the canonical schema:
  ```
  {"timestamp": "21/08/2026, 09:12:04", "level": "INFO", "user_id": "101",
   "method": "GET", "endpoint": "/login", "status_code": 200, "response_time": 12.3}
  ```
- Sample routes (`/login`, `/products`, `/payment`) accept a `user_id`
  query param, enabling real multi-user traffic.

