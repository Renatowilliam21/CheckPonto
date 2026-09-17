$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " ATENCAO - RESET DO BANCO CHECKPONTO"
Write-Host "============================================================"
Write-Host ""
Write-Host "Este comando remove o volume local de desenvolvimento."
Write-Host "Todos os dados locais do PostgreSQL serao apagados."
Write-Host ""

$resposta = Read-Host "Digite RESET para continuar"

if ($resposta -ne "RESET") {
    Write-Host "Operacao cancelada."
    exit 0
}

docker compose down -v

Write-Host ""
Write-Host "[OK] Banco local removido."
Write-Host "Execute scripts/development/start-database.ps1 para recriar."
