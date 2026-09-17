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
.\scripts\development\start-database.ps1
```

Validar:

```powershell
.\scripts\development\validate-database.ps1
```

Parar:

```powershell
.\scripts\development\stop-database.ps1
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
