# How to Run the NRPT App (Simple Steps)

## What "run the app from the folder" means

When you run a command in **CMD** (or PowerShell), you are always "in" some folder — that folder is called your **current directory**.  
Python looks for the `backend` package **inside that current directory**.  
So **"run the app from the folder"** means: **before** you run the uvicorn command, make sure your current directory is the **project folder** — the one that **contains** the `backend` folder.

---

## Step-by-step

### 1. Find the right folder

You need the folder that **contains** a subfolder named **`backend`**.

- If you opened this project in **Cursor**, that folder is usually something like:
  - `C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery`
- In **File Explorer**, open that folder and check: you should see **`backend`** (and also `README.md`, `requirements.txt`, etc.). That folder is the **project root**.

### 2. Open CMD

- Press **Win + R**, type **cmd**, press Enter,  
  **or**
- In Cursor: **Terminal → New Terminal**.

### 3. Go to that folder in CMD

Type (replace with your actual path if different):

```cmd
cd /d C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery
```

Press **Enter**.  
You are now "in" the project folder. The next command will run **from** this folder.

### 4. Start the app

Type:

```cmd
uvicorn backend.app.main:app --reload --port 5000
```

Press **Enter**.  
You should see something like: `Uvicorn running on http://127.0.0.1:5000`.

### 5. Open the app in your browser

- **Load fresh data:** http://127.0.0.1:5000/seed_fresh  
- **Login:** http://127.0.0.1:5000/login  
  - Email: **architect@nrpt.com**  
  - Password: **password**

---

## Even simpler: use the batch file

If you have a file named **`run_nrpt.bat`** in the **same folder** that contains **`backend`**:

1. In File Explorer, go to that folder (the one that contains `backend`).
2. Double-click **`run_nrpt.bat`**.

That will open CMD, go to the right folder, and start the app on port 5000.  
Then open http://127.0.0.1:5000/seed_fresh and http://127.0.0.1:5000/login in your browser.

---

## Why it failed before

When you ran:

```cmd
C:\Mac\Home\Desktop\Ashram-Processes\Nursery> uvicorn backend.app.main:app --reload --port 5000
```

your current directory was **`C:\Mac\Home\Desktop\Ashram-Processes\Nursery`**.  
That folder did **not** contain a **`backend`** subfolder (only the docx/xlsx files), so Python said **"No module named 'backend'"**.

Running **from the folder** means: first **cd** into the folder that **does** contain **`backend`**, **then** run the same uvicorn command.
