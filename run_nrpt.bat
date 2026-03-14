@echo off
REM Run NRPT from the folder that contains 'backend'
cd /d "%~dp0"
if not exist "backend\app\main.py" (
    echo ERROR: backend folder not found. Run this from the project root that contains backend.
    pause
    exit /b 1
)
echo Starting NRPT on http://127.0.0.1:5000
echo Open: http://127.0.0.1:5000/seed_fresh then http://127.0.0.1:5000/login
uvicorn backend.app.main:app --reload --port 5000
pause
