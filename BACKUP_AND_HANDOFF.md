# NRPT — Backup & Handoff (Resume Tomorrow)

**Date:** Session backup for resuming work tomorrow.  
**Source:** NRPT.docx (Nursery Resource & Progress Tracker); all progress built in this project.

---

## 1. What Was Built

- **NRPT MVP**: Web app for managing 50+ landscaping/nursery projects — dashboard heat maps, WBS, BOQ/BOM, defects, approvals, role-based access (Architect, Project Owner, Supervisor, Field Manager).
- **Backend:** FastAPI + SQLite (SQLModel), JWT auth (cookie), RBAC.
- **Frontend:** Server-rendered Jinja2 templates + static CSS (dark theme).
- **Data:** 10 demo projects with full WBS trees, BOQ at WBS level, and defects (seed data in `backend/app/seed_data.py`).

---

## 2. Project Structure (Where the Code Lives)

```
Nursery/                          ← Project root (must run uvicorn FROM HERE)
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               ← All routes (login, dashboard, projects, WBS, BOQ, defects, approvals, users)
│   │   ├── auth.py               ← JWT, password hash (PBKDF2), require_roles
│   │   ├── config.py             ← JWT secret, sqlite path (nrpt.db)
│   │   ├── db.py                 ← SQLite engine, create_db_and_tables(), migration for defect.wbs_item_id
│   │   ├── models.py             ← User, Project, WbsItem, BoqItem, Defect, DefectAttachment, enums
│   │   └── seed_data.py          ← 10 projects, WBS template, BOQ template, defects template; seed_demo_projects()
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── base.html, login.html, dashboard.html, projects.html, project_detail.html
│       ├── wbs.html              ← Tree with expand/collapse, dates, resources
│       ├── boq.html              ← Grouped by WBS, rollup to project budget
│       ├── defects.html          ← Optional WBS link, photo/video/audio upload, status workflow
│       ├── approvals.html, users.html, report_defect.html
├── requirements.txt
├── README.md
├── run_nrpt.bat                  ← Starts uvicorn on port 5000 from this folder
├── nrpt.db                       ← SQLite DB (created on first run)
├── NRPT.docx                     ← Original spec
├── NRPT_extracted.txt            ← Text extracted from NRPT.docx (reference)
└── BACKUP_AND_HANDOFF.md         ← This file
```

**Important:** The folder you `cd` into before running `uvicorn` **must** contain the `backend` folder. Otherwise you get `ModuleNotFoundError: No module named 'backend'`.

---

## 3. How to Run (Critical for Tomorrow)

1. **Open CMD and go to the project root** (the folder that contains `backend`):
   - If you use Cursor’s copy of the project:
     ```cmd
     cd /d C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery
     ```
   - If you copied the project elsewhere, `cd` to that folder instead.

2. **Start the app:**
   ```cmd
   uvicorn backend.app.main:app --reload --port 5000
   ```
   Or double‑click `run_nrpt.bat` in that same folder.

3. **In the browser:**
   - Fresh DB: **http://127.0.0.1:5000/seed_fresh** (or `/seed-fresh`)
   - Login: **http://127.0.0.1:5000/login**  
   Demo logins: `architect@nrpt.com` / `owner@nrpt.com` / `supervisor@nrpt.com` / `field@nrpt.com` — password: **password**

---

## 4. Issues We Hit & Fixes

| Issue | Fix |
|-------|-----|
| Port 8002: "access forbidden" / WinError 10013 | Use another port, e.g. **5000**: `uvicorn ... --port 5000` |
| `/seed-fresh` returns 404 | Route exists; restart server from the folder that contains `backend`. Also added `/seed_fresh` (underscore). |
| `ModuleNotFoundError: No module named 'backend'` | Run uvicorn from the **project root** (folder that contains `backend`), not from a different path (e.g. not from `C:\Mac\Home\Desktop\Ashram-Processes\Nursery` if that copy has no `backend`). |
| Defects page Internal Server Error | Added migration in `db.py` to add `defect.wbs_item_id`; fixed None handling for `wbs_name` and DefectAttachment load. |
| WBS/BOQ "shows nothing" | Fixed owner-name None in `build_wbs_tree`; BOQ grouped by WBS with safe `wbs_by_id` lookup. Re-seed via `/seed_fresh` for full data. |

---

## 5. Features Implemented (Summary)

- **Auth:** Login (form + cookie), logout, 4 roles; Field Manager cannot see prices in BOQ.
- **Dashboard:** Heat map (green/yellow/red), total budget/actual/variance; Architect/Owner only.
- **Projects:** CRUD, executive summary (4 sections), budget/actual/progress.
- **WBS:** Tree with expand/collapse, start/end dates, primary/secondary owner names, weight %, status; add item with parent/dates.
- **BOQ/BOM:** Per-project; materials at WBS/activity level; grouped by WBS with subtotals; rollup to project budget vs actual.
- **Defects:** Optional link to WBS/task; photo/video/audio upload (stored base64); status: open, in_progress, pending_approval, resolved, closed, reopened, cancelled, approved.
- **Approvals:** Queue of WBS items in `pending_approval`; approve/reject (reason required for reject).
- **Users:** List (Architect only).
- **Public defect report:** `/report-defect` — no login.
- **Seed:** `/seed` = ensure users + 10 projects (by name). **`/seed_fresh`** = clear all data, then load 4 users + 10 projects with full WBS, BOQ, defects.

---

## 6. Where to Resume Tomorrow

1. **Get the app running**
   - From project root (folder with `backend`):  
     `uvicorn backend.app.main:app --reload --port 5000`
   - If your daily path is `C:\Mac\Home\Desktop\Ashram-Processes\Nursery`, either run from the Cursor project path above or **copy the whole project** (including `backend`) to that path and run from there.

2. **Load fresh data**
   - Open **http://127.0.0.1:5000/seed_fresh** once.

3. **Smoke test**
   - Login as `architect@nrpt.com` / `password`
   - Check Dashboard, Projects, WBS (tree), BOQ (grouped by WBS), Defects (create one, upload a file, change status).

4. **Possible next steps** (from NRPT.docx / backlog)
   - Excel import/export for WBS and BOQ
   - Gantt view
   - Notifications (e.g. WhatsApp/Email)
   - Offline/PWA
   - QR for public defect reporting

---

## 7. Key URLs (port 5000)

| URL | Purpose |
|-----|--------|
| http://127.0.0.1:5000/seed_fresh | Clear DB and load 10 projects + full data |
| http://127.0.0.1:5000/seed | Add users + projects if missing |
| http://127.0.0.1:5000/login | Login |
| http://127.0.0.1:5000/ | Dashboard (Architect/Owner) or redirect |
| http://127.0.0.1:5000/projects | Projects list |
| http://127.0.0.1:5000/wbs | WBS tree |
| http://127.0.0.1:5000/boq | BOQ by WBS |
| http://127.0.0.1:5000/defects | Defects |
| http://127.0.0.1:5000/approvals | Approvals queue |
| http://127.0.0.1:5000/report-defect | Public defect form (no login) |

---

## 8. Demo Users (password: `password`)

- **architect@nrpt.com** — Full access; Users page; create projects/WBS/BOQ; see all costs.
- **owner@nrpt.com** — Dashboard, projects, WBS, BOQ, approvals; see all costs.
- **supervisor@nrpt.com** — WBS, BOQ, defects, approvals; no Users; no cost visibility in BOQ (optional).
- **field@nrpt.com** — WBS (status to pending_approval), BOQ (actual qty only, **no prices**), defects.

---

*Backup complete. Resume by running from the correct folder and hitting `/seed_fresh` then `/login`.*
