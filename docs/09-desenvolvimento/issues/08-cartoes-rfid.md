# Issue 08 — [RFID] Implementar gestão de cartões RFID

## Objetivo
Cadastrar cartões e controlar sua atribuição aos participantes.

## Requisitos relacionados
- RF12, RF13, RF14
- RN02
- UC05
- CT24

## Escopo
- cadastrar UID;
- listar;
- atribuir a participante;
- bloquear/ativar;
- preservar histórico de atribuição.

## Critérios de aceitação
- [ ] UID é normalizado;
- [ ] cartão ativo possui associação válida;
- [ ] bloqueio impede geração de ponto válido;
- [ ] histórico de atribuição é preservado;
- [ ] duplicidades indevidas são rejeitadas.

## Dependências
Issue 05.

## Testes esperados
Cadastro, UID duplicado, atribuição, bloqueio e histórico.
