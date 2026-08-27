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

### Next
Phase 1 — **Refactor current code**: port `main.py` analytics into the
`analytics/` package as pure, testable functions and route report output
through `reports/report.py`.
