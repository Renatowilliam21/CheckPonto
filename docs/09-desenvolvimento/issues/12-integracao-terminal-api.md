# Issue 12 — [INTEGRAÇÃO] Enviar evento RFID do terminal para a API

## Objetivo
Realizar a primeira integração ponta a ponta entre ESP32 e backend.

## Requisitos relacionados
- RF17, RF19, RF20, RF26
- RN08, RN09
- RNF02, RNF04, RNF07, RNF08, RNF09
- UC06, UC07
- CT04, CT05, CT22, CT23

## Evento de referência

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

## Escopo
- gerar `event_id`;
- obter timestamp;
- montar JSON;
- autenticar terminal;
- POST para API;
- armazenar EVENTO_RFID;
- impedir duplicidade;
- preparar comportamento para falha de rede.

## Critérios de aceitação
- [ ] evento válido chega ao backend;
- [ ] evento é persistido;
- [ ] mesmo `event_id` retransmitido não duplica;
- [ ] cartão desconhecido não é atribuído incorretamente;
- [ ] falha HTTP é tratada pelo firmware;
- [ ] terminal recebe confirmação adequada.

## Dependências
Issues 01, 08, 09 e 11.

## Testes esperados
CT04, CT05, CT22 e CT23.

## Fora do escopo
Interpretação completa da jornada, que será implementada em etapa posterior.
