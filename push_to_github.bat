@echo off
cd /d "C:\Users\itadmin\.cursor\projects\psf-Home-Desktop-Ashram-Processes-Nursery"
echo Adding and committing...
git add -A
git status --short
git commit -m "Update: WBS upload redirect errors, Projects fix, template fixes" --allow-empty
echo Pushing to GitHub...
git push origin main
echo.
echo Done. If you saw no errors above, check https://github.com/getthirumal-bot/ecotrack/commits/main
if "%1"=="" pause
