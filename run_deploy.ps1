# Open the pages you need to finish deploy (GitHub + Railway)
Start-Process "https://github.com/new?name=ecotrack&description=Ecotrack+Program+%26+Project+Tracker"
Start-Process "https://railway.app"
Write-Host ""
Write-Host "Next: After you create the repo on GitHub (no README), run:" -ForegroundColor Cyan
Write-Host '  git remote add origin https://github.com/YOUR_USERNAME/ecotrack.git'
Write-Host '  git branch -M main'
Write-Host '  git push -u origin main'
Write-Host ""
Write-Host "Then in Railway: New Project -> Deploy from GitHub -> select ecotrack. Add Postgres and set DATABASE_URL + JWT_SECRET. Generate domain." -ForegroundColor Cyan
Write-Host ""
