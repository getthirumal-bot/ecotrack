@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
if not exist .env (
  echo .env not found. Copy .env.example to .env and add your GITHUB_TOKEN.
  exit /b 1
)
for /f "usebackq tokens=2 delims==" %%a in (`findstr /b "GITHUB_TOKEN" .env 2^>nul`) do set "GITHUB_TOKEN=%%a"
if not defined GITHUB_TOKEN (
  echo .env must contain a line: GITHUB_TOKEN=ghp_your_token
  exit /b 1
)
git remote set-url origin "https://getthirumal-bot:!GITHUB_TOKEN!@github.com/getthirumal-bot/ecotrack.git"
echo Remote origin updated. Run "git push origin main" to verify.
endlocal
