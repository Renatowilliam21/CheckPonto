# Protocolo RFID

## Payload inicial

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

## Idempotência

`event_id` deve ser único. Se o mesmo evento for retransmitido, a API não deverá criar uma segunda batida.

## Responsabilidade do terminal

O terminal envia event_id, device_id, UID e timestamp. Ele não decide se o evento representa entrada, saída, intervalo ou retorno.

Essa interpretação é responsabilidade do backend.

## Operação offline

Na ausência de rede, o terminal mantém uma fila local e reenvia os eventos após a recuperação da conexão.
