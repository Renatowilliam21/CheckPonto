# Issue 11 — [HARDWARE] Criar protótipo ESP32 + RC522

## Objetivo
Obter leitura confiável de cartões RFID no terminal físico.

## Requisitos relacionados
- RF16, RF18
- UC06

## Referências
- `docs/06-hardware/`
- `firmware/esp32-rfid-terminal/README.md`

## Escopo
- confirmar placa ESP32;
- confirmar RC522;
- definir e documentar pinagem;
- montar protótipo;
- ler UID;
- normalizar UID;
- fornecer feedback básico.

## Critérios de aceitação
- [ ] pinagem real documentada;
- [ ] UID é lido repetidamente com estabilidade;
- [ ] diferentes cartões são distinguidos;
- [ ] firmware está organizado no repositório;
- [ ] montagem é documentada.

## Dependências
Nenhuma de software.

## Testes esperados
Leituras repetidas, cartões diferentes e ausência de cartão.

## Fora do escopo
Interpretação de entrada/saída.
