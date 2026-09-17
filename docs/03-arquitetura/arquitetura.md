# Arquitetura do CheckPonto

## Visão geral

O CheckPonto adotará uma arquitetura distribuída com terminal RFID, API/backend, PostgreSQL e frontend web.

```text
Cartão RFID -> RC522 -> ESP32 -> API REST -> PostgreSQL
                                      |
                                      +-> Frontend Web
```

## Responsabilidades

O terminal registra fatos observados no ambiente físico e não concentra regras complexas de negócio.

O backend é responsável por autenticação, autorização, validação, interpretação das batidas, cálculo de jornadas, carga semanal, justificativas, relatórios e auditoria.

O frontend consome exclusivamente a API e não acessa diretamente o banco de dados.

## Princípio

O hardware registra fatos. O servidor interpreta os fatos e aplica as regras de negócio.
