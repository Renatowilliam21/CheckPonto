$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "Parando PostgreSQL do CheckPonto..."
docker compose stop postgres
Write-Host "[OK] Comando concluido."
