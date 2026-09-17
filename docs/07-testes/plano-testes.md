# Plano de Testes — CheckPonto

## Objetivo

Validar cada módulo isoladamente e também o fluxo completo do sistema.

## Níveis

### Testes unitários

Aplicados principalmente às regras do backend:

- interpretação de batidas;
- cálculo de jornada;
- intervalo;
- carga semanal;
- calendário;
- justificativas;
- estados do relatório.

### Testes de integração

Validam:

- API + banco;
- autenticação;
- constraints;
- RFID + API;
- backend + banco.

### Testes frontend

Validam:

- formulários;
- permissões;
- estados de carregamento;
- erros;
- fluxos principais.

### Testes hardware

Validam:

- leitura do cartão;
- estabilidade;
- Wi-Fi;
- envio;
- fila offline;
- retransmissão.

### Testes ponta a ponta

Validam cenários completos envolvendo usuário, API, banco e, quando possível,
terminal físico.

## Regra

Uma funcionalidade não deve ser considerada concluída apenas porque a tela
funciona visualmente.

As regras de negócio associadas precisam ser verificadas.
