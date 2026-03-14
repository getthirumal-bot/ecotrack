# Agent Handoff — Read This Before Building

**Agent: After every build, test the changes and give the user clear confirmation (what was done, what was tested, what they need to do).**

**Purpose:** Everything the user asked for is below. Use this as the single source of truth. After any build work, **test the changes** and **give the user clear confirmation** of what was done and what was tested.

---

## 1. Ecotrack Rebrand (UI Only)

- **Goal:** Push this app under "Ecotrack"; domain not bought yet.
- **Scope:** Rebrand only. Change NRPT → Ecotrack and "Nursery Resource & Progress Tracker" → **"Program & Project Tracker"** everywhere the user sees it.
- **Files to change:**
  - `backend/app/config.py` — `app_name` = "Ecotrack"
  - `backend/app/main.py` — FastAPI(title="Ecotrack"); optional: seed user emails to *@ecotrack.com and "as in NRPT" → "as in Ecotrack"
  - `backend/templates/base.html` — title default "Ecotrack", brand-mark "Ecotrack", brand-sub "Program & Project Tracker"
  - `backend/templates/login.html` — h1 "Ecotrack"; demo logins *@nrpt.com or *@ecotrack.com (align with main.py)
  - `backend/templates/report_defect.html` — title "Report Defect · Ecotrack", brand-mark "Ecotrack"
  - `backend/app/notifications.py` — all "NRPT" in subject/body/signature → "Ecotrack"; SMTP_FROM default "ecotrack@localhost"
- **Do not change:** cookie name `nrpt_token`, `nrpt.db`, `run_nrpt.bat` (unless user asks later).

---

## 2. Mobile-Ready Web App

- **User intent:** Most users will use the app on mobile (web). Long-term: convert to mobile app. Coding standards and UI should align.
- **UI (now):** Responsive, touch-friendly (min ~44px tap targets), mobile-first for key flows. Check `backend/static/style.css` breakpoints (768px, 480px). Sidebar → hamburger or bottom nav on small screens. Viewport meta in base.html.
- **Code (for future mobile):** Backend API-friendly; consistent JSON responses. Keep logic and UI structure clear so a future mobile client can reuse APIs. Document in README if helpful.

---

## 3. Two Project Types: Implementation vs Maintenance

- **Implementation (current):** Leave as-is. Full dashboard, WBS, BOQ, defects, approvals.
- **Maintenance (new):**
  - **Model:** Project type = `implementation` | `maintenance`. Default existing projects to implementation.
  - **Month-scoped:** Plan and track by month (e.g. project + year-month). Tasks are repetitive.
  - **Copy previous month:** Action to copy last month's task list into next month (and optionally from template).
  - **Separate dashboard:** Maintenance projects only; monthly KPIs; comparison matrix (month vs month, plan vs actual).
  - **Navigation:** Separate entry for "Maintenance" dashboard / projects. Filter project lists by type where relevant.

---

## 4. Hosting and Production

- **Recommendation:** Single platform (Railway or Render), one deployment for the full FastAPI app. GitHub for repo. Add **PostgreSQL** for production (not SQLite on ephemeral disk).
- **Domain:** Not required to share the app. Platform gives a URL (e.g. *.railway.app or *.onrender.com). User can add custom domain (e.g. ecotrack.com) later.
- **To push current version to production:** Add Postgres support (DATABASE_URL), production run instructions, deploy guide (e.g. HOSTING.md). User provides: platform choice (Railway or Render), GitHub repo, and sets JWT_SECRET + DATABASE_URL on the host.

---

## 5. Build Order (When User Approves)

1. **Phase 1:** Ecotrack rebrand (all UI/config/notifications).
2. **Phase 2:** Mobile-ready UI pass (responsive, touch, nav).
3. **Phase 3:** Two project types + maintenance (model, monthly plan, copy month, maintenance dashboard, comparison matrix).
4. **Phase 4:** Postgres support, deploy guide, production setup.

For "push this version to production" only: Postgres + deploy guide + platform connect; no need to do rebrand/maintenance first unless user says so.

---

## 6. Agent Rules

- **Before building:** Confirm which phase(s) or task(s) the user approved.
- **After building:** Run relevant tests (e.g. start app, smoke-test changed pages, run any existing tests). Fix any regressions.
- **Handoff to user:** Reply with: (1) what was done, (2) what was tested, (3) any steps the user must do (e.g. set env vars, run migrations), (4) how to verify (e.g. open /login, check Ecotrack title).

---

*Last updated from user conversation: Ecotrack rebrand, mobile-ready, two project types, hosting on Railway/Render, production deploy, and "agent must test and give confirmation".*
