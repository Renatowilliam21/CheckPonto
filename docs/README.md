# Índice Geral da Documentação — CheckPonto

## 01 — Visão

- [Visão geral](01-visao/visao-geral.md)
- [Escopo](01-visao/escopo.md)
- [Atores](01-visao/atores.md)

## 02 — Requisitos

- [Índice de requisitos](02-requisitos/README.md)
- [Regras de negócio](02-requisitos/regras-negocio.md)
- [Requisitos funcionais](02-requisitos/requisitos-funcionais.md)
- [Requisitos não funcionais](02-requisitos/requisitos-nao-funcionais.md)
- [Casos de uso](02-requisitos/casos-de-uso.md)

## 03 — Arquitetura

- [Visão da arquitetura](03-arquitetura/arquitetura.md)
- [Componentes](03-arquitetura/componentes.md)
- [Decisões arquiteturais](03-arquitetura/decisoes-arquiteturais.md)
- [Fluxos do sistema](03-arquitetura/fluxos-sistema.md)

## 04 — Banco de Dados

- [Modelo de domínio](04-banco-dados/modelo-dominio.md)
- [Modelo lógico](04-banco-dados/modelo-logico.md)
- [Dicionário de dados](04-banco-dados/dicionario-dados.md)
- [ERD](../database/diagrams/erd.md)

## 05 — API

- [Índice da API](05-api/README.md)
- [Endpoints](05-api/endpoints.md)
- [Padrões de resposta](05-api/padroes-resposta.md)
- [Autenticação e autorização](05-api/autenticacao-autorizacao.md)
- [Protocolo RFID](05-api/protocolo-rfid.md)

## 06 — Hardware

- [Índice de hardware](06-hardware/README.md)
- [Componentes](06-hardware/componentes.md)
- [Pinagem](06-hardware/pinagem.md)
- [Montagem](06-hardware/montagem.md)
- [Firmware](06-hardware/firmware.md)

## 07 — Testes

- [Índice de testes](07-testes/README.md)
- [Plano de testes](07-testes/plano-testes.md)
- [Casos de teste](07-testes/casos-testes.md)
- [Matriz de rastreabilidade](07-testes/matriz-rastreabilidade.md)

## 08 — Implantação

A documentação desta área representa orientações para etapas posteriores e
não é pré-requisito para os alunos iniciarem a implementação.

## 09 — Desenvolvimento

- [Índice](09-desenvolvimento/README.md)
- [Guia dos alunos](09-desenvolvimento/guia-alunos.md)
- [Divisão dos módulos](09-desenvolvimento/divisao-modulos.md)
- [Roteiro de 3 meses](09-desenvolvimento/roteiro-3-meses.md)
- [Backlog inicial](09-desenvolvimento/backlog-inicial.md)

---

## Ordem recomendada para novos integrantes

```text
Visão
  -> Requisitos
      -> Arquitetura
          -> Módulo atribuído
              -> Banco/API/Hardware relacionado
                  -> Casos de teste
                      -> Issue
                          -> Desenvolvimento
```
