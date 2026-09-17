from pathlib import Path
import shutil
import sys
from datetime import datetime

ROOT = Path.cwd()

def fail(msg):
    print(f"[ERRO] {msg}")
    sys.exit(1)

def write_file(rel, content):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    if not path.exists() or path.stat().st_size == 0:
        fail(f"Falha ao gravar: {rel}")
    print(f"[OK] {rel} ({path.stat().st_size} bytes)")

def backup_if_exists(rel):
    path = ROOT / rel
    if not path.exists() or path.stat().st_size == 0:
        return None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = ROOT / "database" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / f"{path.name}.{stamp}.bak"
    shutil.copy2(path, dest)
    print(f"[OK] Backup: {dest.relative_to(ROOT)}")
    return dest

print()
print("=" * 76)
print(" CHECKPONTO - SCRIPT 03 - POSTGRESQL EXECUTAVEL")
print("=" * 76)
print()

required = [
    "database/schema_initial.sql",
    "database/migrations",
    "database/seeds",
    "scripts/setup",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"Etapa anterior ausente ou projeto incorreto: {rel}")

schema_source = ROOT / "database/schema_initial.sql"
schema = schema_source.read_text(encoding="utf-8")

if schema.count("CREATE TABLE ") != 24:
    fail(
        "schema_initial.sql nao possui as 24 tabelas esperadas. "
        f"Encontradas: {schema.count('CREATE TABLE ')}"
    )

print("[OK] Modelo SQL inicial localizado.")
print("[OK] 24 tabelas confirmadas.")
print()

# -------------------------------------------------------------------
# Migration oficial
# -------------------------------------------------------------------

migration_header = """-- ============================================================
-- CHECKPONTO
-- Migration 001 - Esquema inicial
--
-- Regra:
-- Este arquivo representa a primeira versao oficial do schema.
-- Depois de aplicado em ambientes compartilhados, nao deve ser
-- reescrito; alteracoes futuras devem usar novas migrations.
-- ============================================================

BEGIN;

"""

migration_footer = """

COMMIT;
"""

migration = migration_header + schema.strip() + migration_footer

backup_if_exists("database/migrations/001_initial_schema.sql")
write_file("database/migrations/001_initial_schema.sql", migration)

# -------------------------------------------------------------------
# Seeds
# -------------------------------------------------------------------

write_file("database/seeds/001_tipos_vinculo.sql", """
-- CHECKPONTO
-- Seed inicial dos tipos de vinculo.
--
-- Duracoes sao armazenadas em minutos.

INSERT INTO tipo_vinculo (
    nome,
    carga_semanal_padrao_min,
    carga_diaria_minima_min,
    carga_diaria_maxima_min,
    ativo
)
VALUES
    (
        'BOLSISTA',
        960,
        240,
        360,
        TRUE
    ),
    (
        'ESTAGIARIO',
        0,
        240,
        480,
        TRUE
    )
ON CONFLICT (nome) DO NOTHING;
""")

write_file("database/seeds/README.md", """
# Seeds — CheckPonto

## 001_tipos_vinculo.sql

Cria os tipos iniciais:

- BOLSISTA;
- ESTAGIARIO.

Para BOLSISTA:

- carga semanal padrão: 960 minutos = 16 horas;
- carga diária mínima de referência: 240 minutos = 4 horas;
- carga diária máxima de referência: 360 minutos = 6 horas.

Para ESTAGIARIO:

- a carga semanal padrão permanece 0 porque deve ser definida no vínculo;
- carga diária mínima de referência: 240 minutos = 4 horas;
- carga diária máxima de referência: 480 minutos = 8 horas.

Os valores são parâmetros iniciais e poderão ser alterados pela aplicação
sem modificar o firmware.
""")

# -------------------------------------------------------------------
# Docker Compose
# -------------------------------------------------------------------

backup_if_exists("docker-compose.yml")

write_file("docker-compose.yml", """
services:
  postgres:
    image: postgres:16-alpine
    container_name: checkponto-postgres
    restart: unless-stopped

    environment:
      POSTGRES_DB: ${POSTGRES_DB:-checkponto}
      POSTGRES_USER: ${POSTGRES_USER:-checkponto}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-checkponto_dev}

    ports:
      - "${POSTGRES_PORT:-5432}:5432"

    volumes:
      - checkponto_postgres_data:/var/lib/postgresql/data
      - ./database/migrations/001_initial_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql:ro
      - ./database/seeds/001_tipos_vinculo.sql:/docker-entrypoint-initdb.d/02-seed-tipos-vinculo.sql:ro

    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -U ${POSTGRES_USER:-checkponto} -d ${POSTGRES_DB:-checkponto}"
        ]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 5s

volumes:
  checkponto_postgres_data:
""")

# -------------------------------------------------------------------
# Environment examples
# -------------------------------------------------------------------

backup_if_exists(".env.example")

write_file(".env.example", """
# ============================================================
# CheckPonto - Ambiente de desenvolvimento
# ============================================================

POSTGRES_DB=checkponto
POSTGRES_USER=checkponto
POSTGRES_PASSWORD=checkponto_dev
POSTGRES_PORT=5432

# Futuro backend
DATABASE_URL=postgresql://checkponto:checkponto_dev@localhost:5432/checkponto

# Fuso de negocio usado inicialmente pela aplicacao.
APP_TIMEZONE=America/Fortaleza
""")

write_file("backend/.env.example", """
NODE_ENV=development
PORT=3000

DATABASE_URL=postgresql://checkponto:checkponto_dev@localhost:5432/checkponto

APP_TIMEZONE=America/Fortaleza

# Gerar valores reais no ambiente local.
JWT_SECRET=trocar_esta_chave_em_desenvolvimento
""")

# -------------------------------------------------------------------
# Scripts auxiliares Windows/PowerShell
# -------------------------------------------------------------------

write_file("scripts/development/start-database.ps1", r"""
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
""")

write_file("scripts/development/stop-database.ps1", r"""
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "Parando PostgreSQL do CheckPonto..."
docker compose stop postgres
Write-Host "[OK] Comando concluido."
""")

write_file("scripts/development/status-database.ps1", r"""
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host " CHECKPONTO - STATUS POSTGRESQL"
Write-Host "============================================================"
Write-Host ""

docker compose ps postgres
""")

write_file("scripts/development/reset-database.ps1", r"""
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
""")

# -------------------------------------------------------------------
# Validação SQL executável por psql dentro do container
# -------------------------------------------------------------------

write_file("database/scripts/validate_database.sql", """
\\echo '============================================================'
\\echo ' CHECKPONTO - VALIDACAO DO BANCO'
\\echo '============================================================'

SELECT current_database() AS banco_atual;

SELECT COUNT(*) AS tabelas_checkponto
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE';

\\echo ''
\\echo 'Tipos de vinculo:'

SELECT
    id,
    nome,
    carga_semanal_padrao_min,
    carga_diaria_minima_min,
    carga_diaria_maxima_min,
    ativo
FROM tipo_vinculo
ORDER BY id;

\\echo ''
\\echo 'Verificando event_uuid UNIQUE:'

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'evento_rfid'
  AND indexdef ILIKE '%event_uuid%';

\\echo ''
\\echo 'Tabelas:'

SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
""")

write_file("scripts/development/validate-database.ps1", r"""
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
""")

# -------------------------------------------------------------------
# Guia da etapa
# -------------------------------------------------------------------

write_file("docs/08-implantacao/postgresql-local.md", """
# PostgreSQL Local — CheckPonto

## Pré-requisito

Docker Desktop com Docker Compose disponível.

## Subir o banco

No PowerShell, a partir da raiz:

```powershell
.\\scripts\\development\\start-database.ps1
```

## Consultar status

```powershell
.\\scripts\\development\\status-database.ps1
```

## Validar

```powershell
.\\scripts\\development\\validate-database.ps1
```

A validação deve mostrar 24 tabelas e os tipos BOLSISTA e ESTAGIARIO.

## Parar

```powershell
.\\scripts\\development\\stop-database.ps1
```

## Reset local

Somente em desenvolvimento:

```powershell
.\\scripts\\development\\reset-database.ps1
```

O reset remove o volume local e apaga todos os dados.

## Importante sobre docker-entrypoint-initdb.d

Os arquivos montados em `/docker-entrypoint-initdb.d` são executados pelo
PostgreSQL somente quando o volume de dados é criado pela primeira vez.

Por isso, durante o desenvolvimento inicial, alterações na migration ou seed
exigem recriação do volume local para serem aplicadas automaticamente.

Depois que o projeto adotar um mecanismo formal de migrations no backend,
não dependeremos desse comportamento para evoluções do schema.
""")

# -------------------------------------------------------------------
# Atualizar database README
# -------------------------------------------------------------------

write_file("database/README.md", """
# Banco de Dados — CheckPonto

## Tecnologia

PostgreSQL 16.

## Estrutura

- `schema_initial.sql` — rascunho lógico preservado;
- `migrations/001_initial_schema.sql` — primeira migration oficial;
- `seeds/001_tipos_vinculo.sql` — dados iniciais;
- `scripts/validate_database.sql` — validação do banco;
- `diagrams/erd.md` — ERD Mermaid;
- `backups/` — backups produzidos pelos scripts de preparação.

## Desenvolvimento local

Subir:

```powershell
.\\scripts\\development\\start-database.ps1
```

Validar:

```powershell
.\\scripts\\development\\validate-database.ps1
```

Parar:

```powershell
.\\scripts\\development\\stop-database.ps1
```

## Política de migrations

Uma migration aplicada em ambiente compartilhado não deve ser reescrita.

Alterações futuras deverão gerar:

- `002_...sql`;
- `003_...sql`;
- e assim sucessivamente.

## Regras estruturais

- 24 tabelas iniciais;
- eventos RFID brutos preservados;
- `event_uuid` único;
- durações em minutos;
- `TIMESTAMPTZ` para eventos temporais;
- sem `ON DELETE CASCADE` no histórico;
- auditoria com JSONB;
- segredos dos terminais armazenados como hash.
""")

# -------------------------------------------------------------------
# Validação estática do que foi gerado
# -------------------------------------------------------------------

print()
print("=" * 76)
print(" VALIDACAO ESTATICA")
print("=" * 76)

files = [
    "database/migrations/001_initial_schema.sql",
    "database/seeds/001_tipos_vinculo.sql",
    "database/scripts/validate_database.sql",
    "docker-compose.yml",
    ".env.example",
    "backend/.env.example",
    "scripts/development/start-database.ps1",
    "scripts/development/stop-database.ps1",
    "scripts/development/status-database.ps1",
    "scripts/development/reset-database.ps1",
    "scripts/development/validate-database.ps1",
    "docs/08-implantacao/postgresql-local.md",
]

errors = 0

for rel in files:
    p = ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        print(f"[ERRO] {rel}")
        errors += 1
    else:
        print(f"[OK] {rel} ({p.stat().st_size} bytes)")

migration_text = (ROOT / "database/migrations/001_initial_schema.sql").read_text(
    encoding="utf-8"
)

table_count = migration_text.count("CREATE TABLE ")
print()
print(f"Tabelas na migration: {table_count}/24")
if table_count != 24:
    errors += 1

checks = [
    ("BEGIN", "BEGIN;" in migration_text),
    ("COMMIT", "COMMIT;" in migration_text),
    ("event_uuid UNIQUE", "event_uuid VARCHAR(120) NOT NULL UNIQUE" in migration_text),
    ("JSONB auditoria", "dados_anteriores JSONB" in migration_text and "dados_novos JSONB" in migration_text),
    ("Sem CASCADE", "ON DELETE CASCADE" not in migration_text),
]

for label, ok in checks:
    print(f"[{'OK' if ok else 'ERRO'}] {label}")
    if not ok:
        errors += 1

seed_text = (ROOT / "database/seeds/001_tipos_vinculo.sql").read_text(
    encoding="utf-8"
)

for name in ["BOLSISTA", "ESTAGIARIO"]:
    ok = f"'{name}'" in seed_text
    print(f"[{'OK' if ok else 'ERRO'}] Seed {name}")
    if not ok:
        errors += 1

compose_text = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
for marker in [
    "postgres:16-alpine",
    "checkponto-postgres",
    "001_initial_schema.sql",
    "001_tipos_vinculo.sql",
    "healthcheck:",
]:
    ok = marker in compose_text
    print(f"[{'OK' if ok else 'ERRO'}] docker-compose: {marker}")
    if not ok:
        errors += 1

print()

if errors:
    print("=" * 76)
    print(f" CONFIGURACAO FINALIZADA COM {errors} PROBLEMA(S)")
    print("=" * 76)
    sys.exit(1)

print("=" * 76)
print(" POSTGRESQL PREPARADO COM SUCESSO")
print("=" * 76)
print("Migration: database/migrations/001_initial_schema.sql")
print("Seed:      database/seeds/001_tipos_vinculo.sql")
print("Container: checkponto-postgres")
print()
print("PROXIMO PASSO MANUAL:")
print("  .\\scripts\\development\\start-database.ps1")
print()
print("DEPOIS:")
print("  .\\scripts\\development\\validate-database.ps1")
print()
