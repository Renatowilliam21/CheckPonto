# Hardware e Firmware

## Leia nesta ordem

1. [Componentes](componentes.md);
2. [Pinagem](pinagem.md);
3. [Montagem](montagem.md);
4. [Firmware](firmware.md);
5. [Protocolo RFID](../05-api/protocolo-rfid.md).

## Meta inicial da equipe

Primeiro obter uma leitura confiável:

```text
Cartão -> RC522 -> ESP32
```

Depois evoluir para:

```text
Cartão -> RC522 -> ESP32 -> API
```

Somente depois adicionar fila offline, feedback e demais recursos.

A pinagem definitiva deverá ser documentada após confirmação do hardware
real disponível.
