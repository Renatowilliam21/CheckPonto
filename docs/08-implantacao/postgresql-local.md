# PostgreSQL Local — CheckPonto

## Pré-requisito

Docker Desktop com Docker Compose disponível.

## Subir o banco

No PowerShell, a partir da raiz:

```powershell
.\scripts\development\start-database.ps1
```

## Consultar status

```powershell
.\scripts\development\status-database.ps1
```

## Validar

```powershell
.\scripts\development\validate-database.ps1
```

A validação deve mostrar 24 tabelas e os tipos BOLSISTA e ESTAGIARIO.

## Parar

```powershell
.\scripts\development\stop-database.ps1
```

## Reset local

Somente em desenvolvimento:

```powershell
.\scripts\development\reset-database.ps1
```

O reset remove o volume local e apaga todos os dados.

## Importante sobre docker-entrypoint-initdb.d

Os arquivos montados em `/docker-entrypoint-initdb.d` são executados pelo
PostgreSQL somente quando o volume de dados é criado pela primeira vez.

Por isso, durante o desenvolvimento inicial, alterações na migration ou seed
exigem recriação do volume local para serem aplicadas automaticamente.

Depois que o projeto adotar um mecanismo formal de migrations no backend,
não dependeremos desse comportamento para evoluções do schema.
