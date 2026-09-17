# Terminal RFID — CheckPonto

Firmware do terminal físico do sistema.

## Responsabilidade

```text
Cartão -> RC522 -> ESP32 -> API
```

O firmware coleta o fato físico e transmite o evento.

As regras de jornada permanecem no backend.

## Desenvolvimento sugerido

1. leitura do UID;
2. Wi-Fi;
3. geração de event_id;
4. timestamp;
5. JSON;
6. envio HTTP;
7. feedback;
8. fila offline;
9. sincronização;
10. testes de integração.

Consultar:

- `docs/06-hardware/componentes.md`;
- `docs/06-hardware/pinagem.md`;
- `docs/06-hardware/montagem.md`;
- `docs/06-hardware/firmware.md`;
- `docs/05-api/protocolo-rfid.md`.
