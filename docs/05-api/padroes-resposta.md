# Padrões de Resposta da API

## Sucesso

```json
{
  "data": {
    "id": 1
  }
}
```

## Listagem

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 0
  }
}
```

## Erro de validação

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos.",
    "details": []
  }
}
```

## Códigos HTTP sugeridos

| Código | Uso |
| --- | --- |
| 200 | Consulta/alteração concluída |
| 201 | Recurso criado |
| 204 | Operação sem corpo de resposta |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Sem autorização |
| 404 | Recurso não encontrado |
| 409 | Conflito ou duplicidade |
| 422 | Regra de negócio/validação |
| 500 | Erro interno |

## Idempotência RFID

O reenvio do mesmo `event_id` não deverá produzir uma nova batida.

A API deverá responder de maneira que o terminal consiga considerar o evento
sincronizado mesmo quando ele já tiver sido recebido anteriormente.
