from pathlib import Path
import re
import sys

ROOT = Path.cwd()

def fail(msg):
    print(f"[ERRO] {msg}")
    sys.exit(1)

def write_file(rel, content):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    if not path.exists() or path.stat().st_size == 0:
        fail(f"Falha ao gravar {rel}")
    print(f"[OK] {rel} ({path.stat().st_size} bytes)")

def table(title, col, items):
    lines = [f"# {title}", "", f"| ID | {col} |", "| --- | --- |"]
    for code, desc in items:
        lines.append(f"| **{code}** | {desc} |")
    return "\n".join(lines)

print()
print("=" * 70)
print(" CHECKPONTO - CONFIGURACAO DA DOCUMENTACAO INICIAL")
print("=" * 70)
print()

required = ["docs", "frontend", "backend", "database", "firmware", "infrastructure", "scripts", "tests"]
for d in required:
    if not (ROOT / d).exists():
        fail(f"Execute na raiz do CheckPonto. Diretorio ausente: {d}")

print(f"[OK] Raiz localizada: {ROOT}")
print()

write_file("docs/01-visao/visao-geral.md", """
# CheckPonto — Visão Geral

## 1. Apresentação

O CheckPonto é uma plataforma para acompanhamento de bolsistas e estagiários vinculados a laboratórios.

O sistema integra controle de frequência por RFID, acompanhamento da carga horária, registro das atividades desenvolvidas e geração de relatórios.

A solução será composta por aplicação web, API REST, banco de dados, terminal RFID baseado em ESP32 e infraestrutura de implantação.

## 2. Problema

O acompanhamento manual da frequência dificulta a verificação da carga horária efetivamente cumprida e a associação entre o período de permanência no laboratório e as atividades desenvolvidas.

O sistema busca reduzir problemas relacionados a esquecimento de registros, divergências de horários, controle da carga semanal, justificativas, acompanhamento das atividades, consolidação de relatórios e rastreabilidade das correções.

## 3. Objetivo geral

Desenvolver uma plataforma integrada para registrar, acompanhar e consolidar a frequência, a carga horária e as atividades desenvolvidas por bolsistas e estagiários de laboratório.

## 4. Objetivos específicos

- registrar presença utilizando RFID;
- calcular automaticamente a carga horária realizada;
- permitir programação semanal individual;
- acompanhar o cumprimento da carga horária;
- registrar atividades desenvolvidas diariamente;
- consolidar atividades em relatórios semanais;
- controlar faltas e justificativas;
- considerar feriados, recessos e afastamentos;
- permitir correções controladas de ponto;
- fornecer dashboards;
- gerar relatórios por participante e período;
- preservar o histórico das operações relevantes.

## 5. Arquitetura geral

```text
Cartão RFID -> RC522 -> ESP32 -> API REST -> PostgreSQL
                                      |
                                      +-> Aplicação Web
```

## 6. Usuários

Inicialmente o sistema atenderá coordenadores, bolsistas e estagiários. A arquitetura deverá permitir expansão futura para outros laboratórios e tipos de vínculo.
""")

write_file("docs/01-visao/escopo.md", """
# Escopo do CheckPonto

## 1. Gestão

A primeira versão deverá contemplar autenticação, participantes, laboratórios, projetos, tipos de vínculo, cartões RFID e terminais.

## 2. Frequência

O sistema deverá controlar entrada, saída, intervalo de almoço, retorno, cálculo diário e semanal, inconsistências, operação offline temporária e sincronização posterior.

## 3. Planejamento

O coordenador poderá definir uma programação semanal individual para cada participante e comparar carga programada, registrada, calculada e saldo.

## 4. Ocorrências

O sistema deverá tratar faltas justificadas e não justificadas, feriados, recessos, afastamentos e solicitações de correção de ponto.

## 5. Atividades

Cada participante deverá registrar as atividades desenvolvidas por dia. A carga horária será obtida automaticamente do ponto e não digitada pelo participante.

Ao final da semana haverá um resumo semanal e submissão para análise do coordenador.

## 6. Relatórios

Deverão existir relatórios semanais, mensais e por período, contendo carga prevista, realizada, saldo, atividades, ocorrências e resumos.

## 7. Fora do escopo inicial

Não fazem parte obrigatória da primeira versão:

- reconhecimento facial;
- biometria;
- aplicativo mobile nativo;
- folha de pagamento;
- controle financeiro de bolsas;
- geolocalização;
- inteligência artificial;
- WhatsApp ou Telegram;
- integração com sistemas institucionais;
- assinatura digital certificada.
""")

write_file("docs/01-visao/atores.md", """
# Atores do Sistema

## Coordenador

Responsável pela administração do laboratório, participantes, vínculos, projetos, cartões RFID, programações semanais, justificativas, correções, relatórios e dashboards.

## Participante

Representa bolsistas e estagiários. Pode consultar sua programação e carga horária, registrar atividades, preencher resumo semanal, enviar relatório, apresentar justificativas e solicitar correções.

## Terminal RFID

Dispositivo baseado em ESP32 responsável por ler o UID, gerar um identificador único, registrar data/hora, transmitir o evento, fornecer feedback e manter uma fila offline para sincronização posterior.
""")

rn = [
("RN01","Todo participante deverá possuir vínculo ativo com um laboratório para registrar ponto."),
("RN02","Cada cartão RFID ativo deverá estar associado a um único participante."),
("RN03","O participante poderá possuir tipos de vínculo, inicialmente Bolsista ou Estagiário."),
("RN04","Bolsistas terão como regra inicial carga obrigatória de 16 horas semanais."),
("RN05","A programação semanal do bolsista será definida pelo coordenador, considerando normalmente jornadas entre 4 e 6 horas por dia."),
("RN06","Estagiários poderão possuir programação variável, incluindo jornadas previstas de 4 ou 8 horas."),
("RN07","As regras de carga horária serão configuradas no servidor conforme o vínculo e não fixadas no firmware."),
("RN08","O registro oficial de presença será originado prioritariamente pelo RFID."),
("RN09","O participante não selecionará manualmente se a batida representa entrada ou saída."),
("RN10","Uma jornada sem intervalo poderá ser composta por entrada e saída."),
("RN11","Uma jornada com almoço deverá considerar saída e retorno do intervalo."),
("RN12","O intervalo de almoço não será contabilizado como tempo trabalhado."),
("RN13","Batidas incompletas ou inconsistentes deverão gerar ocorrência."),
("RN14","O participante não poderá alterar diretamente um registro originado pelo RFID."),
("RN15","Correções de ponto deverão ser solicitadas pelo participante e analisadas pelo coordenador."),
("RN16","Toda correção deverá preservar o registro original e seu histórico."),
("RN17","A carga realizada será calculada a partir dos registros válidos e das correções aprovadas."),
("RN18","Cada participante deverá possuir programação semanal individual."),
("RN19","Feriados e recessos não deverão gerar automaticamente falta ou carga pendente."),
("RN20","Afastamentos individuais não deverão produzir faltas durante sua vigência."),
("RN21","Ausências poderão ser classificadas como justificadas ou não justificadas."),
("RN22","As justificativas deverão ser analisadas pelo coordenador."),
("RN23","O participante deverá registrar a descrição das atividades desenvolvidas diariamente."),
("RN24","A carga horária apresentada junto à atividade será obtida automaticamente do controle de ponto."),
("RN25","O participante deverá registrar um resumo semanal das atividades."),
("RN26","O sistema deverá consolidar automaticamente carga prevista e realizada no fechamento semanal."),
("RN27","O relatório semanal poderá assumir os estados EM_PREENCHIMENTO, ENVIADO, APROVADO e DEVOLVIDO."),
("RN28","Um relatório devolvido poderá ser corrigido e reenviado."),
("RN29","Alterações posteriores à aprovação deverão ser controladas e registradas."),
("RN30","O sistema deverá manter histórico de registros, correções, justificativas e aprovações."),
]
write_file("docs/02-requisitos/regras-negocio.md", table("Regras de Negócio", "Regra", rn))

rf_desc = [
"Permitir autenticação por login e senha.",
"Permitir ao coordenador cadastrar, consultar, alterar e desativar participantes.",
"Permitir atribuir perfis de acesso aos usuários.",
"Permitir ao participante consultar suas informações individuais.",
"Impedir acesso não autorizado aos dados individuais de outros participantes.",
"Permitir cadastrar e gerenciar laboratórios.",
"Permitir associar coordenadores aos laboratórios.",
"Permitir cadastrar projetos.",
"Permitir associar participantes aos projetos.",
"Permitir cadastrar tipos de vínculo.",
"Permitir associar vínculos aos participantes.",
"Permitir cadastrar cartões RFID.",
"Permitir associar cartão RFID a participante.",
"Permitir ativar ou bloquear cartão RFID.",
"Permitir cadastrar terminais RFID.",
"Permitir ao terminal identificar o UID do cartão.",
"Permitir ao terminal transmitir eventos para a API.",
"Fornecer confirmação visual ou sonora no terminal.",
"Armazenar temporariamente eventos quando o terminal estiver sem comunicação.",
"Sincronizar eventos pendentes quando a comunicação for restabelecida.",
"Permitir ao coordenador cadastrar programação semanal individual.",
"Permitir definir dias, horários e carga prevista.",
"Calcular carga horária semanal prevista.",
"Permitir programações diferentes conforme o tipo de vínculo.",
"Preservar histórico das programações anteriores.",
"Registrar data, hora, cartão, participante e terminal de cada batida.",
"Interpretar automaticamente a sequência das batidas.",
"Identificar jornadas com e sem intervalo de almoço.",
"Calcular automaticamente a carga horária diária.",
"Descontar o intervalo de almoço da carga realizada.",
"Calcular carga horária semanal realizada.",
"Comparar carga prevista e realizada.",
"Identificar registros incompletos ou inconsistentes.",
"Permitir ao participante solicitar correção de ponto.",
"Exigir justificativa para solicitação de correção.",
"Permitir ao coordenador aprovar ou rejeitar solicitações de correção.",
"Preservar registro original e histórico das correções.",
"Registrar faltas justificadas e não justificadas.",
"Permitir ao participante apresentar justificativa de ausência.",
"Permitir ao coordenador analisar justificativas.",
"Permitir cadastrar feriados.",
"Permitir cadastrar recessos.",
"Permitir cadastrar afastamentos individuais.",
"Considerar calendário, afastamentos e justificativas na situação semanal.",
"Permitir ao participante registrar atividades desenvolvidas diariamente.",
"Relacionar atividade a participante e data.",
"Apresentar automaticamente a carga registrada junto à atividade diária.",
"Impedir alteração manual da carga horária proveniente do ponto.",
"Permitir editar atividade enquanto o período estiver aberto.",
"Permitir registrar resumo semanal.",
"Gerar consolidação semanal automaticamente.",
"Apresentar carga prevista, realizada e saldo.",
"Apresentar registros diários e atividades na consolidação semanal.",
"Permitir ao participante enviar relatório semanal.",
"Permitir ao coordenador aprovar relatório semanal.",
"Permitir ao coordenador devolver relatório com observação.",
"Permitir corrigir e reenviar relatório devolvido.",
"Registrar data e responsável pela aprovação.",
"Disponibilizar dashboard individual do participante.",
"Apresentar progresso da carga semanal.",
"Disponibilizar dashboard administrativo do coordenador.",
"Exibir participantes atualmente presentes no laboratório.",
"Exibir carga prevista e realizada por participante.",
"Identificar participantes com carga horária pendente.",
"Identificar atividades diárias ainda não preenchidas.",
"Exibir relatórios semanais pendentes de análise.",
"Exibir ocorrências e solicitações de correção pendentes.",
"Permitir consultar registros por participante e período.",
"Gerar relatório semanal individual.",
"Gerar relatório mensal individual.",
"Gerar relatório para período personalizado.",
"Apresentar carga prevista e realizada nos relatórios.",
"Apresentar atividades desenvolvidas nos relatórios.",
"Apresentar resumos semanais nos relatórios.",
"Apresentar ocorrências relevantes nos relatórios.",
"Permitir exportar relatórios em PDF.",
]
rf = [(f"RF{i:02d}", desc) for i, desc in enumerate(rf_desc, 1)]
write_file("docs/02-requisitos/requisitos-funcionais.md", table("Requisitos Funcionais", "Requisito", rf))

rnf_desc = [
"A aplicação web deverá possuir interface responsiva.",
"A comunicação entre terminal e servidor deverá utilizar API HTTP/HTTPS.",
"Senhas não poderão ser armazenadas em texto puro.",
"A API deverá exigir autenticação dos terminais RFID.",
"O sistema deverá implementar controle de acesso baseado em perfil.",
"Operações administrativas relevantes deverão possuir auditoria.",
"O terminal deverá armazenar temporariamente eventos durante indisponibilidade da rede.",
"A sincronização deverá ser idempotente e não produzir registros duplicados.",
"Data e hora deverão possuir origem controlada e consistente.",
"O sistema deverá preservar integridade e rastreabilidade dos registros de frequência.",
"O sistema deverá adotar medidas adequadas de proteção de dados pessoais.",
"O código-fonte deverá ser versionado utilizando Git.",
]
rnf = [(f"RNF{i:02d}", desc) for i, desc in enumerate(rnf_desc, 1)]
write_file("docs/02-requisitos/requisitos-nao-funcionais.md", table("Requisitos Não Funcionais", "Requisito", rnf))

write_file("docs/03-arquitetura/arquitetura.md", """
# Arquitetura do CheckPonto

## Visão geral

O CheckPonto adotará uma arquitetura distribuída com terminal RFID, API/backend, PostgreSQL e frontend web.

```text
Cartão RFID -> RC522 -> ESP32 -> API REST -> PostgreSQL
                                      |
                                      +-> Frontend Web
```

## Responsabilidades

O terminal registra fatos observados no ambiente físico e não concentra regras complexas de negócio.

O backend é responsável por autenticação, autorização, validação, interpretação das batidas, cálculo de jornadas, carga semanal, justificativas, relatórios e auditoria.

O frontend consome exclusivamente a API e não acessa diretamente o banco de dados.

## Princípio

O hardware registra fatos. O servidor interpreta os fatos e aplica as regras de negócio.
""")

write_file("docs/03-arquitetura/componentes.md", """
# Componentes do Sistema

## Frontend
React + TypeScript + Vite.

## Backend
Node.js + TypeScript + API REST.

## Banco de dados
PostgreSQL.

## Firmware
ESP32 + RC522 + PlatformIO.

Componentes previstos: display OLED, buzzer, LEDs e RTC DS3231.

## Infraestrutura
Docker, Docker Compose e Nginx.

## Engenharia
Git, GitHub, Issues, Pull Requests e GitHub Actions.
""")

write_file("docs/03-arquitetura/decisoes-arquiteturais.md", """
# Decisões Arquiteturais

## DA01 — Monorepo
Frontend, backend, firmware, banco, infraestrutura, documentação e testes permanecerão inicialmente no mesmo repositório.

## DA02 — API REST
Frontend e terminal se comunicarão com o backend por HTTP/HTTPS.

## DA03 — PostgreSQL
O PostgreSQL será o banco relacional principal.

## DA04 — Regras no servidor
Regras de jornada não serão fixadas no firmware.

## DA05 — Evento RFID imutável
O evento bruto recebido do terminal será preservado mesmo quando sua interpretação mudar.

## DA06 — Duração em minutos
Durações serão armazenadas como minutos inteiros.

## DA07 — Idempotência
Cada evento terá identificador único. Retransmissões não poderão criar duplicatas.

## DA08 — Auditoria
Correções, justificativas, aprovações e operações administrativas relevantes deverão preservar histórico.
""")

write_file("docs/04-banco-dados/modelo-dominio.md", """
# Modelo de Domínio

## Entidades

### Usuario
Conta de acesso ao sistema.

### Laboratorio
Unidade acompanhada pelo sistema.

### Participante
Bolsista ou estagiário.

### TipoVinculo
Define categorias e regras gerais de carga horária.

### Vinculo
Relaciona participante e tipo de vínculo em determinado período.

### Projeto
Projeto ou atividade desenvolvida no laboratório.

### ParticipanteProjeto
Associação entre participante e projeto.

### CartaoRFID
Cartão físico associado ao participante. O UID deve ser único.

### Terminal
Terminal ESP32/RFID instalado no laboratório.

### Programacao
Programação semanal vigente do participante.

### ProgramacaoDia
Horários e carga prevista por dia.

### EventoRFID
Evento bruto e imutável recebido do hardware.

### RegistroPonto
Interpretação do evento: ENTRADA, SAIDA_INTERVALO, RETORNO_INTERVALO ou SAIDA.

### JornadaDiaria
Carga prevista, realizada, saldo e situação de um dia.

### AtividadeDiaria
Descrição das atividades. Não possui horas editáveis.

### RelatorioSemanal
Consolida período, carga, saldo, resumo e aprovação.

### EventoCalendario
FERIADO, RECESSO ou SUSPENSAO.

### Afastamento
Período individual de afastamento.

### Justificativa
Justificativa de ausência.

### SolicitacaoAjuste
Pedido de correção de ponto.

### Auditoria
Histórico das operações administrativas relevantes.

## Princípio de rastreabilidade

O CheckPonto separa:

1. EVENTO_RFID — fato observado pelo hardware;
2. REGISTRO_PONTO — interpretação;
3. JORNADA_DIARIA — consolidação.

Isso permite reinterpretar uma sequência de batidas sem destruir o dado original.
""")

write_file("docs/05-api/protocolo-rfid.md", """
# Protocolo RFID

## Payload inicial

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

## Idempotência

`event_id` deve ser único. Se o mesmo evento for retransmitido, a API não deverá criar uma segunda batida.

## Responsabilidade do terminal

O terminal envia event_id, device_id, UID e timestamp. Ele não decide se o evento representa entrada, saída, intervalo ou retorno.

Essa interpretação é responsabilidade do backend.

## Operação offline

Na ausência de rede, o terminal mantém uma fila local e reenvia os eventos após a recuperação da conexão.
""")

write_file("README.md", """
# CheckPonto

Sistema de acompanhamento de bolsistas e estagiários de laboratório com registro de frequência por RFID.

## Arquitetura

```text
Cartão RFID -> RC522 -> ESP32 -> API REST -> PostgreSQL
                                      |
                                      +-> Aplicação Web
```

## Tecnologias propostas

- Frontend: React + TypeScript + Vite
- Backend: Node.js + TypeScript
- Banco: PostgreSQL
- Firmware: ESP32 + RC522 + PlatformIO
- Infraestrutura: Docker + Docker Compose + Nginx

## Estrutura

- `frontend/` — aplicação web
- `backend/` — API e regras de negócio
- `database/` — banco, migrations e seeds
- `firmware/` — terminal ESP32/RFID
- `infrastructure/` — implantação
- `tests/` — testes globais
- `scripts/` — automação
- `docs/` — documentação
- `.github/` — padrões e CI

## Fluxo Git

Issue -> Branch -> Commits -> Pull Request -> Revisão -> main

## Status

Projeto em fase inicial de especificação e desenvolvimento.
""")

print()
print("=" * 70)
print(" VALIDACAO")
print("=" * 70)

errors = 0
checks = [
    ("RN", len(rn), 30),
    ("RF", len(rf), 76),
    ("RNF", len(rnf), 12),
]
for name, got, expected in checks:
    status = "OK" if got == expected else "ERRO"
    print(f"[{status}] {name}: {got}/{expected}")
    if got != expected:
        errors += 1

for rel in [
    "README.md",
    "docs/01-visao/visao-geral.md",
    "docs/01-visao/escopo.md",
    "docs/01-visao/atores.md",
    "docs/02-requisitos/regras-negocio.md",
    "docs/02-requisitos/requisitos-funcionais.md",
    "docs/02-requisitos/requisitos-nao-funcionais.md",
    "docs/03-arquitetura/arquitetura.md",
    "docs/03-arquitetura/componentes.md",
    "docs/03-arquitetura/decisoes-arquiteturais.md",
    "docs/04-banco-dados/modelo-dominio.md",
    "docs/05-api/protocolo-rfid.md",
]:
    p = ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        print(f"[ERRO] {rel}")
        errors += 1

print()
if errors:
    print(f"[ERRO] Finalizado com {errors} problema(s).")
    sys.exit(1)

print("=" * 70)
print(" DOCUMENTACAO INICIAL CONFIGURADA COM SUCESSO")
print("=" * 70)
print("RN: 30 | RF: 76 | RNF: 12")
print("Proxima etapa: modelo logico PostgreSQL, ERD e dicionario de dados.")
