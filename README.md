# CheckPonto

**Sistema de Acompanhamento de Bolsistas e Estagiários com Registro de Frequência por RFID**

O CheckPonto é um projeto acadêmico de desenvolvimento de software e sistemas
embarcados para acompanhamento de bolsistas e estagiários vinculados a
laboratórios.

A plataforma integra frequência por RFID, carga horária, atividades
desenvolvidas, justificativas, correções, relatórios e acompanhamento pelo
coordenador.

---

## Para os alunos: comece aqui

Antes de escrever código:

1. leia [Visão Geral](docs/01-visao/visao-geral.md);
2. leia [Escopo](docs/01-visao/escopo.md);
3. conheça os [Atores](docs/01-visao/atores.md);
4. consulte os [Requisitos](docs/02-requisitos/README.md);
5. compreenda a [Arquitetura](docs/03-arquitetura/README.md);
6. consulte o [Guia dos Alunos](docs/09-desenvolvimento/guia-alunos.md);
7. identifique seu módulo em [Divisão dos Módulos](docs/09-desenvolvimento/divisao-modulos.md);
8. consulte o [Backlog Inicial](docs/09-desenvolvimento/backlog-inicial.md);
9. trabalhe por Issue, branch e Pull Request;
10. implemente, teste e atualize a documentação.

> Não iniciar o desenvolvimento apenas pela interface. Primeiro identifique o
> requisito, o caso de uso, o modelo de dados e o contrato da API relacionados
> à funcionalidade.

---

## Arquitetura geral

```text
                      +----------------------+
                      |     Frontend Web     |
                      | React + TypeScript   |
                      +----------+-----------+
                                 |
                                 | HTTP/JSON
                                 v
+---------+     +-------+     +----------------------+     +------------+
| Cartão  | --> | RC522 | --> | ESP32 / Terminal    | --> |            |
|  RFID   |     +-------+     +----------------------+     |            |
                                                           |  API REST  |
                                                           |            |
                      +----------------------+              |  Backend   |
                      |     PostgreSQL       | <----------> |            |
                      +----------------------+              +------------+
```

Princípio central:

**o hardware registra fatos; o servidor interpreta os fatos e aplica as
regras de negócio.**

---

## Principais funcionalidades

- autenticação;
- participantes;
- laboratórios;
- vínculos;
- projetos;
- cartões RFID;
- terminais;
- programação semanal individual;
- registro de frequência;
- cálculo de jornada;
- controle de intervalo;
- carga semanal;
- atividades diárias;
- justificativas;
- ajustes de ponto;
- feriados e recessos;
- afastamentos;
- relatórios semanais;
- aprovação/devolução;
- dashboards;
- auditoria.

---

## Estrutura do repositório

```text
CheckPonto/
|
+-- frontend/             Aplicação web
+-- backend/              API e regras de negócio
+-- database/             Modelo, migrations, seeds e diagramas
+-- firmware/             Terminal ESP32/RFID
+-- infrastructure/       Arquivos de infraestrutura
+-- tests/                Testes globais e integração
+-- scripts/              Scripts auxiliares
+-- docs/                 Documentação do projeto
+-- .github/              Issues, PRs e automações
+-- CONTRIBUTING.md       Regras de contribuição
+-- README.md             Porta de entrada do projeto
```

---

## Mapa da documentação

| Área | Conteúdo |
| --- | --- |
| `docs/01-visao` | problema, objetivos, escopo e atores |
| `docs/02-requisitos` | RN, RF, RNF e casos de uso |
| `docs/03-arquitetura` | arquitetura, componentes, decisões e fluxos |
| `docs/04-banco-dados` | domínio, modelo lógico e dicionário |
| `docs/05-api` | endpoints, respostas, autenticação e RFID |
| `docs/06-hardware` | ESP32, RC522, firmware e montagem |
| `docs/07-testes` | plano, casos e rastreabilidade |
| `docs/08-implantacao` | orientações futuras de implantação |
| `docs/09-desenvolvimento` | guia dos alunos, módulos, backlog e cronograma |

Consulte também o [Índice Geral](docs/README.md).

---

## Requisitos já especificados

- 30 Regras de Negócio;
- 76 Requisitos Funcionais;
- 12 Requisitos Não Funcionais;
- 20 Casos de Uso;
- 25 Casos de Teste iniciais.

---

## Modelo de frequência

O sistema separa três conceitos:

```text
EVENTO_RFID
    |
    v
REGISTRO_PONTO
    |
    v
JORNADA_DIARIA
```

`EVENTO_RFID` representa o fato bruto capturado pelo terminal.

`REGISTRO_PONTO` representa a interpretação desse fato.

`JORNADA_DIARIA` representa a consolidação das horas.

Essa separação preserva rastreabilidade e permite corrigir interpretações sem
destruir os eventos originais.

---

## Fluxo Git

```text
Issue
  -> Branch
      -> Implementação
          -> Testes
              -> Commit
                  -> Push
                      -> Pull Request
                          -> Revisão
                              -> main
```

Não desenvolver diretamente na `main`.

Consulte [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Tecnologias propostas

- Frontend: React + TypeScript + Vite;
- Backend: Node.js + TypeScript;
- Banco: PostgreSQL;
- Firmware: ESP32 + RC522;
- Firmware build: PlatformIO;
- API: REST/JSON;
- Versionamento: Git + GitHub.

A implementação concreta deve seguir a documentação e poderá ser refinada
durante o desenvolvimento.

---

## Planejamento

O MVP foi organizado para aproximadamente 12 semanas.

Consulte:

[docs/09-desenvolvimento/roteiro-3-meses.md](docs/09-desenvolvimento/roteiro-3-meses.md)

---

## Estado atual

A base documental e arquitetural inicial está preparada.

A próxima fase é o desenvolvimento incremental pelos alunos, começando pelas
Issues e módulos definidos no backlog.
