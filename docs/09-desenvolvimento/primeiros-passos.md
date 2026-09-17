# Primeiros Passos do Aluno

## Passo 1 — Entenda o projeto

Leia:

- `README.md`;
- `docs/01-visao/`;
- `docs/02-requisitos/README.md`;
- `docs/03-arquitetura/README.md`.

## Passo 2 — Descubra seu módulo

Consulte:

`docs/09-desenvolvimento/divisao-modulos.md`

## Passo 3 — Identifique os requisitos

Não comece pelo código.

Liste os requisitos e casos de uso associados à tarefa.

## Passo 4 — Consulte os contratos

Dependendo do módulo:

- backend/frontend: `docs/05-api/`;
- banco: `docs/04-banco-dados/`;
- firmware: `docs/06-hardware/`;
- testes: `docs/07-testes/`.

## Passo 5 — Escolha uma Issue

A Issue deve representar uma entrega pequena e verificável.

Evite uma Issue genérica como:

```text
Fazer o sistema de ponto
```

Prefira:

```text
Implementar cadastro de cartão RFID
```

ou:

```text
Implementar tratamento idempotente de evento RFID
```

## Passo 6 — Crie a branch

Exemplo:

```text
feature/cadastro-cartao-rfid
```

## Passo 7 — Desenvolva incrementalmente

Implemente apenas o necessário para atender à Issue.

## Passo 8 — Teste

Consulte os casos existentes e acrescente novos quando necessário.

## Passo 9 — Documente

Se um contrato, comportamento ou decisão mudou, atualize a documentação.

## Passo 10 — Abra Pull Request

Explique:

- o que foi feito;
- requisitos atendidos;
- como testar;
- limitações conhecidas.

A revisão faz parte do desenvolvimento.
