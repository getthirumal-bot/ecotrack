# Ecotrack – Recovery guide (project deleted)

Use this if the **Railway project**, **GitHub repo**, or **app data** was deleted.

---

## Your code is safe here

- **Local folder:** `C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery` (this workspace) has the full Ecotrack app.
- **GitHub:** Code is pushed to **https://github.com/getthirumal-bot/ecotrack** (confirm the repo still exists).

---

## 1. If the **Railway project** was deleted

You need to deploy again from GitHub.

1. Go to **https://railway.app** → **New Project** → **Deploy from GitHub repo**.
2. Select **getthirumal-bot/ecotrack** (or your fork).
3. Add **Postgres:** in the same project click **+ New** → **Database** → **PostgreSQL**.
4. Open your **web service** → **Variables** → add:
   - **DATABASE_URL** (from the Postgres service – use “Add reference” or paste the connection string).
   - **JWT_SECRET** (any long random string).
5. **Settings** → **Networking** → **Generate domain**.
6. Wait for the deploy. Your app will be at `https://xxxx.up.railway.app`.
7. Load data: open **`https://your-app.up.railway.app/seed`** once, then **`/seed-chukapalli`**, then **`/seed-chukapalli-tasks`**. Log in with `architect@nrpt.com` / `password`.

---

## 2. If the **GitHub repo** was deleted

Recreate the repo and push from this folder.

1. On GitHub, create a **new repository** (e.g. **ecotrack**), empty, no README.
2. In PowerShell (or CMD) run:

```powershell
cd "C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery"
git remote set-url origin https://github.com/YOUR_USERNAME/ecotrack.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Then in Railway, either reconnect the same project to this new repo or create a new project and deploy from this repo (and add Postgres + variables as in section 1).

---

## 3. If only **data** was wiped (app still runs, but no users/projects)

The database was reset; the app and repo are fine.

1. Open **`https://your-app.up.railway.app/seed`** once (creates users + demo projects).
2. Open **`https://your-app.up.railway.app/seed-chukapalli`** once (creates Chukapalli maintenance project).
3. Open **`https://your-app.up.railway.app/seed-chukapalli-tasks`** once (adds plantation tasks to Chukapalli).
4. Log in with **architect@nrpt.com** / **password**.

---

## 3b. Data disappears after each deploy (e.g. new maintenance project you created is gone)

If projects or other UI-created data vanish after you push a new version, the app is using **SQLite** (no **DATABASE_URL**). Each deploy gets a new container with an empty database.

**Fix:** Add a **Postgres** database and set **DATABASE_URL** so data persists:

1. In your Railway project: **+ New** → **Database** → **PostgreSQL**.
2. Open your **web service** → **Variables** → add **DATABASE_URL** (use “Add reference” and pick the Postgres service’s `DATABASE_URL`).
3. Redeploy (or push a small change). After that, all UI-created data (projects, maintenance projects, etc.) will persist across deploys.

---

## 4. If your **local folder** was deleted

If you still have the GitHub repo:

```powershell
git clone https://github.com/getthirumal-bot/ecotrack.git
cd ecotrack
```

Then deploy to Railway from this repo (section 1). If the GitHub repo was also deleted, use section 2 after recreating the repo; you may need to recreate the folder from backup or from someone who has a copy.

---

## Quick checklist

| What was deleted? | What to do |
|-------------------|------------|
| Railway project   | New Project → Deploy from GitHub → add Postgres + variables → Generate domain → run /seed, /seed-chukapalli, /seed-chukapalli-tasks |
| GitHub repo        | Create new repo → `git remote set-url origin ...` → `git push -u origin main` → then deploy on Railway |
| Data only          | Visit /seed, /seed-chukapalli, /seed-chukapalli-tasks on your app URL |
| Local folder only  | `git clone` from GitHub (if repo exists) |

---

**Custom domain (ecotrack.ltd):** After you have a new Railway URL, add the custom domain again in Railway (Settings → Networking → Custom domain) and keep your GoDaddy/Cloudflare DNS pointing to the new Railway hostname if needed.
