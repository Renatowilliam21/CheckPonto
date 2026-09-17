# Responsabilidades do Firmware

## Deve fazer

- inicializar componentes;
- conectar ao Wi-Fi;
- ler UID;
- normalizar UID;
- gerar `event_id`;
- obter timestamp;
- montar JSON;
- transmitir evento;
- interpretar resposta HTTP;
- fornecer feedback;
- enfileirar eventos offline;
- tentar sincronização posterior.

## Não deve fazer

O firmware não deve decidir:

- se uma batida é entrada ou saída;
- quantidade semanal obrigatória;
- aprovação de justificativa;
- saldo semanal;
- situação do relatório;
- regras administrativas.

## Evento mínimo

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

## Idempotência

O `event_id` precisa permanecer o mesmo durante retransmissões do mesmo
evento.

Gerar um novo ID em cada tentativa destruiria a proteção contra duplicidade.

## Organização sugerida do firmware

```text
src/
  main.cpp

include/
  config.h
  rfid_reader.h
  network.h
  event_queue.h
  api_client.h
  feedback.h
  clock_service.h
```

A divisão final poderá ser refinada pela equipe.
