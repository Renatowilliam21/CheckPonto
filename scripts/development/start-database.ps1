$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " CHECKPONTO - INICIANDO POSTGRESQL"
Write-Host "============================================================"
Write-Host ""

docker compose up -d postgres

Write-Host ""
Write-Host "Aguardando healthcheck..."
Write-Host ""

$maxTentativas = 30

for ($i = 1; $i -le $maxTentativas; $i++) {

    $status = docker inspect `
        --format='{{.State.Health.Status}}' `
        checkponto-postgres 2>$null

    if ($status -eq "healthy") {
        Write-Host "[OK] PostgreSQL esta saudavel."
        docker compose ps postgres
        exit 0
    }

    Write-Host "Tentativa $i/$maxTentativas - status: $status"
    Start-Sleep -Seconds 2
}

Write-Host "[ERRO] PostgreSQL nao ficou saudavel no tempo esperado."
docker compose logs postgres
exit 1
