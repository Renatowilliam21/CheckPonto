# ERD — CheckPonto

O diagrama abaixo utiliza Mermaid e pode ser renderizado pelo GitHub.

```mermaid
erDiagram
    USUARIO ||--o| PARTICIPANTE : possui
    USUARIO ||--o{ USUARIO_LABORATORIO : autorizado
    LABORATORIO ||--o{ USUARIO_LABORATORIO : possui

    PARTICIPANTE ||--o{ VINCULO : possui
    LABORATORIO ||--o{ VINCULO : recebe
    TIPO_VINCULO ||--o{ VINCULO : classifica

    LABORATORIO ||--o{ PROJETO : possui
    PARTICIPANTE ||--o{ PARTICIPANTE_PROJETO : participa
    PROJETO ||--o{ PARTICIPANTE_PROJETO : inclui

    CARTAO_RFID ||--o{ CARTAO_PARTICIPANTE : atribuicao
    PARTICIPANTE ||--o{ CARTAO_PARTICIPANTE : utiliza

    LABORATORIO ||--o{ TERMINAL : possui
    TERMINAL ||--o{ EVENTO_RFID : produz
    CARTAO_RFID o|--o{ EVENTO_RFID : reconhecido_como

    VINCULO ||--o{ PROGRAMACAO : possui
    PROGRAMACAO ||--o{ PROGRAMACAO_DIA : detalha

    VINCULO ||--o{ REGISTRO_PONTO : possui
    EVENTO_RFID o|--o| REGISTRO_PONTO : interpretado_como

    VINCULO ||--o{ OCORRENCIA_PONTO : gera
    VINCULO ||--o{ JORNADA_DIARIA : consolida
    JORNADA_DIARIA ||--o{ ATIVIDADE_DIARIA : descreve
    PROJETO o|--o{ ATIVIDADE_DIARIA : referencia

    LABORATORIO ||--o{ EVENTO_CALENDARIO : possui

    VINCULO ||--o{ AFASTAMENTO : possui
    VINCULO ||--o{ JUSTIFICATIVA : apresenta
    VINCULO ||--o{ SOLICITACAO_AJUSTE : solicita
    REGISTRO_PONTO o|--o{ SOLICITACAO_AJUSTE : referencia

    VINCULO ||--o{ RELATORIO_SEMANAL : gera

    USUARIO o|--o{ JUSTIFICATIVA : analisa
    USUARIO o|--o{ SOLICITACAO_AJUSTE : analisa
    USUARIO o|--o{ RELATORIO_SEMANAL : aprova
    USUARIO o|--o{ AUDITORIA : executa
```

## Observação

Este ERD representa o modelo lógico inicial. A migration SQL será criada na
etapa seguinte, após a validação deste modelo.
