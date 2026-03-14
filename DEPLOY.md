# Deploy Ecotrack to Railway or Render

Use this to push the **current version** to production and share the link (no custom domain required).

---

## Quick: Deploy to Railway (no laptop needed)

1. **Push your code to GitHub**  
   - If the project isn’t in a repo yet: create a new repo on GitHub, then in your project folder run:
     ```bash
     git init
     git add .
     git commit -m "Ecotrack initial"
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
     git branch -M main
     git push -u origin main
     ```

2. **Create a Railway account**  
   - Go to [railway.app](https://railway.app) and sign in (e.g. with GitHub).

3. **New Project → Deploy from GitHub**  
   - Choose “Deploy from GitHub repo” and select your Ecotrack repo.  
   - Railway will create a **service** from the repo. The repo root must contain `requirements.txt` and the `backend/` folder (this project is already set up that way).

4. **Add Postgres**  
   - In the same project, click **+ New** → **Database** → **PostgreSQL**.  
   - After it’s created, open the Postgres service → **Variables** and copy `DATABASE_URL`.

5. **Connect Postgres to your app**  
   - Open your **web service** (the one from GitHub), go to **Variables**.  
   - Click **+ New Variable** → **Add a variable reference** and add `DATABASE_URL` from the Postgres service (Railway can link it).  
   - Add another variable: `JWT_SECRET` = any long random string (e.g. run `openssl rand -hex 32` in a terminal and paste the result).

6. **Start command (optional)**  
   - The repo includes `railway.json` with the correct start command. If you need to set it manually: **Settings** → **Deploy** → Start Command:  
     `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

7. **Public URL**  
   - In your web service go to **Settings** → **Networking** → **Generate domain**.  
   - You’ll get a URL like `https://your-app-name.up.railway.app`.

8. **First use**  
   - Open that URL. If the DB is empty, visit `https://your-app-name.up.railway.app/seed` once to load demo data.  
   - Log in with e.g. `architect@nrpt.com` / `password`. Share the link with your team; no need to run anything on your laptop.

---

## 1. Prepare the repo

- Code in a **GitHub** repo.
- Ensure `requirements.txt` is at project **root** (same folder as `backend/`).

## 2. Create a Postgres database

- **Railway:** New Project → Add **Postgres**. Copy the `DATABASE_URL` from Variables.
- **Render:** Dashboard → New → **PostgreSQL**. Copy **Internal Database URL** (or External if your app runs elsewhere).

## 3. Deploy the app

### Option A: Railway

1. New Project → **Deploy from GitHub** → select your repo.
2. Add **Postgres** (step 2) if not already added.
3. Select the **web service** (your repo). The repo includes **railway.json** so Build/Start are set automatically. If you override in the dashboard:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Watch Paths:** `backend`
4. **Variables:** Add:
   - `DATABASE_URL` = (paste from Postgres service or use variable reference)
   - `JWT_SECRET` = (generate a long random string, e.g. `openssl rand -hex 32`)
5. **Settings → Networking:** Click **Generate domain**. Your app will be at `https://your-app.up.railway.app`.

### Option B: Render

1. **New → Web Service** → connect repo.
2. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** empty (repo root).
3. **Environment:** Add:
   - `DATABASE_URL` = (from your Render Postgres)
   - `JWT_SECRET` = (long random string)
4. Create Web Service. URL will be like `https://your-app.onrender.com`.

## 4. First run

- Open the deployed URL. You may see a 502 for a minute while the app starts.
- If the DB is empty, visit `https://your-app.../seed` once to load demo data (or create users via User management when logged in as architect).
- Log in: e.g. `architect@nrpt.com` / `password` (or your seed users).

## 5. Share the link

- Share the Railway or Render URL with your audience. No domain purchase needed.
- To use a custom domain (e.g. ecotrack.com) later: add it in the platform’s dashboard and point DNS as instructed.

## Troubleshooting

- **502 / App not starting:** Check logs. Ensure Start Command uses `$PORT` and `--host 0.0.0.0`.
- **Database errors:** Ensure `DATABASE_URL` is set and correct. For Railway, use the URL from the Postgres service variables.
- **Static/templates not found:** App must run from **repo root** so `backend/` is the package; Start Command should be as above (no `cd` into backend).
