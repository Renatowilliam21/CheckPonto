$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " CHECKPONTO - VALIDANDO POSTGRESQL"
Write-Host "============================================================"
Write-Host ""

$running = docker inspect `
    --format='{{.State.Running}}' `
    checkponto-postgres 2>$null

if ($running -ne "true") {
    Write-Host "[ERRO] O container checkponto-postgres nao esta em execucao."
    Write-Host "Execute primeiro:"
    Write-Host ".\scripts\development\start-database.ps1"
    exit 1
}

Get-Content .\database\scripts\validate_database.sql -Raw |
    docker exec -i checkponto-postgres `
        psql -U checkponto -d checkponto

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Validacao do banco falhou."
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[OK] Validacao SQL concluida."
