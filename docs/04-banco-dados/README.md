# Banco de Dados

## Documentos

- [Modelo de domínio](modelo-dominio.md);
- [Modelo lógico](modelo-logico.md);
- [Dicionário de dados](dicionario-dados.md);
- [ERD Mermaid](../../database/diagrams/erd.md).

## Modelo central de frequência

```text
EVENTO_RFID -> REGISTRO_PONTO -> JORNADA_DIARIA
```

## Regras importantes

- evento RFID bruto deve ser preservado;
- `event_uuid` deve ser único;
- durações são representadas em minutos;
- correções não apagam o histórico;
- dados administrativos relevantes devem ser auditáveis.

A estrutura SQL disponível no repositório serve como referência inicial para
a implementação.
