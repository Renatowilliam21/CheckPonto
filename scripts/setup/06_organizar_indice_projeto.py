from pathlib import Path
import sys

ROOT = Path.cwd()

def fail(msg):
    print(f"[ERRO] {msg}")
    sys.exit(1)

def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"[OK] {rel} ({p.stat().st_size} bytes)")

print("=" * 78)
print(" CHECKPONTO - SCRIPT 06 - INDICE E MAPA DO PROJETO")
print("=" * 78)

required = [
    "docs/01-visao",
    "docs/02-requisitos",
    "docs/03-arquitetura",
    "docs/04-banco-dados",
    "docs/05-api",
    "docs/06-hardware",
    "docs/07-testes",
    "docs/08-implantacao",
    "docs/09-desenvolvimento",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"Etapa documental incompleta. Ausente: {rel}")

write("README.md", """
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
""")

write("docs/README.md", """
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
""")

write("docs/02-requisitos/README.md", """
# Requisitos

Esta pasta contém a especificação funcional do CheckPonto.

## Documentos

- [Regras de Negócio](regras-negocio.md) — RN01 a RN30;
- [Requisitos Funcionais](requisitos-funcionais.md) — RF01 a RF76;
- [Requisitos Não Funcionais](requisitos-nao-funcionais.md) — RNF01 a RNF12;
- [Casos de Uso](casos-de-uso.md) — UC01 a UC20.

## Como usar

Antes de implementar uma funcionalidade:

1. identifique os RF relacionados;
2. consulte as RN aplicáveis;
3. consulte o caso de uso;
4. verifique as restrições não funcionais;
5. consulte os casos de teste;
6. somente então implemente.

Caso a implementação exija alterar um requisito, a alteração deve ser
discutida e documentada.
""")

write("docs/03-arquitetura/README.md", """
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
""")

write("docs/04-banco-dados/README.md", """
# Banco de Dados

## Documentos

- [Modelo de domínio](modelo-dominio.md);
- [Modelo lógico](modelo-logico.md);
- [Dicionário de dados](dicionario-dados.md);
- [ERD Mermaid](../../database/diagrams/erd.md).

## Modelo central de frequência

```text
EVENTO_RFID -> REGISTRO_PONTO -> JORNADA_DIARIA
```

## Regras importantes

- evento RFID bruto deve ser preservado;
- `event_uuid` deve ser único;
- durações são representadas em minutos;
- correções não apagam o histórico;
- dados administrativos relevantes devem ser auditáveis.

A estrutura SQL disponível no repositório serve como referência inicial para
a implementação.
""")

write("docs/06-hardware/README.md", """
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
""")

write("docs/07-testes/README.md", """
# Testes

## Documentos

- [Plano de Testes](plano-testes.md);
- [Casos de Teste](casos-testes.md);
- [Matriz de Rastreabilidade](matriz-rastreabilidade.md).

## Regra para as equipes

Uma funcionalidade não está concluída apenas porque sua interface funciona.

O aluno deve conseguir responder:

1. qual requisito foi implementado?
2. qual regra de negócio está envolvida?
3. como o comportamento foi testado?
4. qual é o resultado esperado?
5. existe algum caso de erro relevante?

Novos cenários encontrados durante o desenvolvimento devem gerar novos casos
de teste.
""")

write("docs/09-desenvolvimento/primeiros-passos.md", """
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
""")

# Atualiza o índice da pasta de desenvolvimento, preservando foco pedagógico.
write("docs/09-desenvolvimento/README.md", """
# Desenvolvimento — Guia das Equipes

## Comece por aqui

- [Primeiros Passos](primeiros-passos.md)
- [Guia dos Alunos](guia-alunos.md)
- [Divisão dos Módulos](divisao-modulos.md)
- [Roteiro de 3 Meses](roteiro-3-meses.md)
- [Backlog Inicial](backlog-inicial.md)

## Fluxo resumido

```text
Entender
 -> escolher requisito
 -> selecionar Issue
 -> criar branch
 -> implementar
 -> testar
 -> documentar
 -> Pull Request
 -> revisão
```

O objetivo é construir o CheckPonto incrementalmente, com entregas pequenas
e integráveis.
""")

print()
print("=" * 78)
print(" VALIDACAO FINAL DA DOCUMENTACAO")
print("=" * 78)

required_files = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/README.md",
    "docs/01-visao/visao-geral.md",
    "docs/01-visao/escopo.md",
    "docs/01-visao/atores.md",
    "docs/02-requisitos/README.md",
    "docs/02-requisitos/regras-negocio.md",
    "docs/02-requisitos/requisitos-funcionais.md",
    "docs/02-requisitos/requisitos-nao-funcionais.md",
    "docs/02-requisitos/casos-de-uso.md",
    "docs/03-arquitetura/README.md",
    "docs/03-arquitetura/arquitetura.md",
    "docs/03-arquitetura/fluxos-sistema.md",
    "docs/04-banco-dados/README.md",
    "docs/04-banco-dados/modelo-dominio.md",
    "docs/04-banco-dados/modelo-logico.md",
    "docs/04-banco-dados/dicionario-dados.md",
    "docs/05-api/README.md",
    "docs/05-api/endpoints.md",
    "docs/05-api/protocolo-rfid.md",
    "docs/06-hardware/README.md",
    "docs/06-hardware/componentes.md",
    "docs/06-hardware/pinagem.md",
    "docs/06-hardware/montagem.md",
    "docs/06-hardware/firmware.md",
    "docs/07-testes/README.md",
    "docs/07-testes/plano-testes.md",
    "docs/07-testes/casos-testes.md",
    "docs/07-testes/matriz-rastreabilidade.md",
    "docs/09-desenvolvimento/README.md",
    "docs/09-desenvolvimento/primeiros-passos.md",
    "docs/09-desenvolvimento/guia-alunos.md",
    "docs/09-desenvolvimento/divisao-modulos.md",
    "docs/09-desenvolvimento/roteiro-3-meses.md",
    "docs/09-desenvolvimento/backlog-inicial.md",
]

errors = 0
for rel in required_files:
    p = ROOT / rel
    if p.exists() and p.stat().st_size > 0:
        print(f"[OK] {rel}")
    else:
        print(f"[ERRO] {rel}")
        errors += 1

print()
print(f"Documentos essenciais encontrados: {len(required_files) - errors}/{len(required_files)}")

if errors:
    print(f"[ERRO] Existem {errors} arquivo(s) ausente(s).")
    sys.exit(1)

print()
print("=" * 78)
print(" REPOSITORIO DOCUMENTAL ORGANIZADO COM SUCESSO")
print("=" * 78)
print("O README.md agora e a porta de entrada dos alunos.")
print("O projeto possui indice geral e roteiro de primeiros passos.")
print("Nenhum servico foi instalado ou executado.")
print()
print("Base pronta para iniciar a organizacao das Issues de desenvolvimento.")
