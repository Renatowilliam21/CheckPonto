# Arquitetura

## Documentos

- [Arquitetura](arquitetura.md);
- [Componentes](componentes.md);
- [Decisões arquiteturais](decisoes-arquiteturais.md);
- [Fluxos do sistema](fluxos-sistema.md).

## Visão resumida

```text
Frontend -> API -> Banco
              ^
              |
         ESP32/RFID
```

## Regra central

O ESP32 captura eventos.

O backend aplica regras de negócio.

O frontend apresenta e manipula dados por meio da API.

O banco preserva os dados e o histórico.

Não mover regras administrativas para o firmware apenas para facilitar uma
implementação local.
