# Montagem do Terminal

## Etapa 1 — Protótipo mínimo

Montar somente:

```text
ESP32 <-> RC522
```

Objetivo: ler o UID de cartões de forma confiável.

## Etapa 2 — Comunicação

Adicionar Wi-Fi e testar envio de um evento simulado para a API.

## Etapa 3 — Feedback

Adicionar LEDs, buzzer e/ou OLED conforme disponibilidade.

## Etapa 4 — Tempo

Adicionar estratégia de sincronização de relógio e, se adotado, RTC DS3231.

## Etapa 5 — Operação offline

Implementar fila local de eventos pendentes.

## Etapa 6 — Integração

Executar o fluxo:

```text
Cartão -> RC522 -> ESP32 -> API -> Banco -> Dashboard
```

## Critério de aceitação do protótipo

O terminal deve conseguir:

- identificar cartão;
- gerar evento único;
- registrar timestamp;
- enviar evento;
- reconhecer confirmação;
- não perder evento em falha temporária de rede;
- retransmitir sem duplicar o registro no servidor.
