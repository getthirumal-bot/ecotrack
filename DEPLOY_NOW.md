# Deploy Ecotrack to Railway — do this now

Your project is committed and ready. Follow these steps to get it off your laptop.

---

## Step 1: Create a GitHub repo (one-time)

1. Open: **https://github.com/new**
2. **Repository name:** `ecotrack` (or any name you like)
3. Choose **Private** or **Public**
4. **Do not** add a README, .gitignore, or license (we already have them)
5. Click **Create repository**

---

## Step 2: Push this folder to GitHub

In PowerShell (or CMD), run these commands. **Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.**

```powershell
cd "C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery"

git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ecotrack.git
git branch -M main
git push -u origin main
```

If you use a different repo name than `ecotrack`, use it in the URL instead.

If Git asks for credentials: use a **Personal Access Token** as the password (GitHub → Settings → Developer settings → Personal access tokens).

---

## Step 3: Deploy on Railway

1. Open: **https://railway.app**
2. Sign in with **GitHub**
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your **ecotrack** (or your repo name) repo
5. In the new project, click **+ New** → **Database** → **PostgreSQL**
6. Click your **web service** (the one from the repo) → **Variables** tab:
   - Add variable: **`DATABASE_URL`** → choose **Add reference** and pick the Postgres `DATABASE_URL` from the database service
   - Add variable: **`JWT_SECRET`** → paste any long random string (e.g. run in PowerShell: `[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }) -as [byte[]])`)
7. In the web service go to **Settings** → **Networking** → **Generate domain**
8. Wait for the deploy to finish. Your app will be at **https://something.up.railway.app**
9. Open that URL. If the DB is empty, visit **https://your-url.up.railway.app/seed** once, then log in with `architect@nrpt.com` / `password`

Done. You can close your laptop; the app runs on Railway.

---

## Data disappears after deploy?

If projects or UI-created data (e.g. a new maintenance project) vanish after you push a new version, the app is using SQLite because **DATABASE_URL** is not set. Add **Postgres** (step 5 above) and set **DATABASE_URL** (step 6). After that, data persists across deploys.
