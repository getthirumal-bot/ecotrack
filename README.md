# NRPT (Nursery Resource & Progress Tracker) — MVP

**Backup & handoff:** See **`BACKUP_AND_HANDOFF.md`** for full progress summary, how to run, issues we fixed, and where to resume.

This is a runnable MVP based on the `NRPT.docx` requirements: projects, WBS weightage, BOQ/BOM with **financial masking**, defects + public QR defect reporting, approvals queue, and an executive dashboard.

## Run locally (Windows)

From the repo root:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

If you get **"socket access forbidden"** or **port in use**, try another port: `--port 8080` or `--port 8003`.

Then open (replace `8000` with your port if different):
- **Fresh DB (recommended)** — `http://127.0.0.1:8000/seed-fresh` — clears all data and loads 10 projects with full WBS, BOQ, and defects.
- Or `http://127.0.0.1:8000/seed` (adds demo users + 10 projects only if DB is empty or missing projects).
- `http://127.0.0.1:8000/login`

## Fresh DB with all 10 projects and supporting data

Visit **`http://127.0.0.1:8000/seed-fresh`** once (use your port if you chose 8080, etc.). This will:
1. Clear all existing data (users, projects, WBS, BOQ, defects, attachments).
2. Repopulate with 4 demo users and 10 projects, each with:
   - Full WBS tree (milestones → sub-milestones → tasks)
   - BOQ/BOM at WBS level (18 materials per project)
   - 5 defects per project

Use this whenever you want a clean slate with all scenarios covered.

## Demo users

Password for all: `password`

- Architect: `architect@nrpt.com`
- Project Owner: `owner@nrpt.com`
- Supervisor/QA: `supervisor@nrpt.com`
- Field Manager: `field@nrpt.com`

## Demo data (after /seed)

- **10 projects** at different phases: active, on_hold, completed; budgets from ~₹4L to ₹2.4Cr.
- **Multi-level WBS** per project: 4 milestones → sub-milestones → tasks (earthwork, irrigation, plantation, hardscape).
- **BOQ/BOM**: 18 materials per project (topsoil, pipes, drippers, plants, labour, etc.) with estimated/actual quantities and unit prices; some variance for realism.
- **Defects**: 5 defects per project (various severities and statuses).

Projects include: Mundra Port Landscaping, Central Park Renovation, Highway Green Belt, Corporate Campus, Township Parks, Institutional Campus (on hold), Riverfront Promenade, Industrial Zone (completed), Airport Approach, Botanical Garden Extension.

## Quick test checklist

- **Architect / Owner**
  - Dashboard shows health-colored tiles and budget/actual/variance rollups.
  - Create a project in Projects.
  - Add WBS items; set weights and owners.
  - Add BOQ items with unit prices.
- **Field Manager**
  - BOQ page: can update actual quantity but **cannot see prices/costs**.
  - WBS page: can set status to `pending_approval` but cannot approve/reject.
- **Supervisor/QA**
  - Approvals page: approve/reject items in `pending_approval`.
- **Public**
  - `http://127.0.0.1:8000/report-defect` submits a defect without login.

