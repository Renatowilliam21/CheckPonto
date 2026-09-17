# Decisões Arquiteturais

## DA01 — Monorepo
Frontend, backend, firmware, banco, infraestrutura, documentação e testes permanecerão inicialmente no mesmo repositório.

## DA02 — API REST
Frontend e terminal se comunicarão com o backend por HTTP/HTTPS.

## DA03 — PostgreSQL
O PostgreSQL será o banco relacional principal.

## DA04 — Regras no servidor
Regras de jornada não serão fixadas no firmware.

## DA05 — Evento RFID imutável
O evento bruto recebido do terminal será preservado mesmo quando sua interpretação mudar.

## DA06 — Duração em minutos
Durações serão armazenadas como minutos inteiros.

## DA07 — Idempotência
Cada evento terá identificador único. Retransmissões não poderão criar duplicatas.

## DA08 — Auditoria
Correções, justificativas, aprovações e operações administrativas relevantes deverão preservar histórico.
