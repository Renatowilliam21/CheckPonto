$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " CHECKPONTO - STATUS POSTGRESQL"
Write-Host "============================================================"
Write-Host ""

docker compose ps postgres
