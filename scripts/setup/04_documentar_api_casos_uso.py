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

print("=" * 76)
print(" CHECKPONTO - SCRIPT 04 - API E CASOS DE USO")
print("=" * 76)

for d in ["docs/05-api", "docs/02-requisitos", "docs/03-arquitetura"]:
    if not (ROOT / d).exists():
        fail(f"Execute na raiz do CheckPonto. Ausente: {d}")

write("docs/05-api/endpoints.md", """
# Endpoints Planejados — CheckPonto

> Este documento é uma especificação inicial para orientar o desenvolvimento.
> Os endpoints poderão ser refinados durante a implementação, desde que as
> mudanças sejam documentadas.

Base sugerida: `/api/v1`.

## 1. Autenticação

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| POST | `/auth/login` | Autenticar usuário |
| GET | `/auth/me` | Consultar usuário autenticado |

## 2. Participantes

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/participantes` | Listar participantes |
| POST | `/participantes` | Cadastrar participante |
| GET | `/participantes/:id` | Consultar participante |
| PATCH | `/participantes/:id` | Atualizar participante |
| PATCH | `/participantes/:id/status` | Alterar situação |

## 3. Laboratórios

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/laboratorios` | Listar laboratórios |
| POST | `/laboratorios` | Cadastrar laboratório |
| GET | `/laboratorios/:id` | Consultar laboratório |
| PATCH | `/laboratorios/:id` | Atualizar laboratório |

## 4. Vínculos

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/vinculos` | Listar vínculos |
| POST | `/vinculos` | Criar vínculo |
| GET | `/vinculos/:id` | Consultar vínculo |
| PATCH | `/vinculos/:id` | Atualizar vínculo |
| PATCH | `/vinculos/:id/encerrar` | Encerrar vínculo |

## 5. Projetos

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/projetos` | Listar projetos |
| POST | `/projetos` | Cadastrar projeto |
| GET | `/projetos/:id` | Consultar projeto |
| PATCH | `/projetos/:id` | Atualizar projeto |
| POST | `/projetos/:id/participantes` | Associar participante |

## 6. Cartões RFID

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/cartoes` | Listar cartões |
| POST | `/cartoes` | Cadastrar cartão |
| POST | `/cartoes/:id/atribuir` | Atribuir cartão |
| PATCH | `/cartoes/:id/bloquear` | Bloquear cartão |

## 7. Terminais

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/terminais` | Listar terminais |
| POST | `/terminais` | Cadastrar terminal |
| GET | `/terminais/:id` | Consultar terminal |
| PATCH | `/terminais/:id` | Atualizar terminal |

## 8. Ingestão RFID

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| POST | `/rfid/eventos` | Receber evento do ESP32 |

Exemplo:

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

A API deverá tratar `event_id` de forma idempotente.

## 9. Programação semanal

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/vinculos/:id/programacoes` | Histórico |
| POST | `/vinculos/:id/programacoes` | Criar programação |
| GET | `/programacoes/:id` | Consultar programação |

## 10. Ponto e jornadas

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/pontos` | Consultar registros |
| GET | `/jornadas` | Consultar jornadas |
| GET | `/jornadas/:id` | Detalhar jornada |
| GET | `/ocorrencias-ponto` | Consultar inconsistências |

## 11. Atividades

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/atividades` | Consultar atividades |
| POST | `/atividades` | Registrar atividade |
| PATCH | `/atividades/:id` | Editar descrição |

A carga horária não deve ser recebida como campo editável da atividade.

## 12. Justificativas e ajustes

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| POST | `/justificativas` | Enviar justificativa |
| GET | `/justificativas` | Consultar justificativas |
| PATCH | `/justificativas/:id/analisar` | Aprovar/rejeitar |
| POST | `/ajustes-ponto` | Solicitar correção |
| GET | `/ajustes-ponto` | Consultar solicitações |
| PATCH | `/ajustes-ponto/:id/analisar` | Aprovar/rejeitar |

## 13. Calendário e afastamentos

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/calendario` | Consultar eventos |
| POST | `/calendario` | Cadastrar evento |
| POST | `/afastamentos` | Cadastrar afastamento |
| GET | `/afastamentos` | Consultar afastamentos |

## 14. Relatórios semanais

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/relatorios-semanais` | Listar |
| GET | `/relatorios-semanais/:id` | Detalhar |
| POST | `/relatorios-semanais/:id/enviar` | Enviar |
| POST | `/relatorios-semanais/:id/aprovar` | Aprovar |
| POST | `/relatorios-semanais/:id/devolver` | Devolver |

## 15. Dashboards

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/dashboard/participante` | Dados do participante |
| GET | `/dashboard/coordenador` | Dados administrativos |
| GET | `/dashboard/presentes` | Participantes presentes |

## 16. Convenções

- JSON como formato principal;
- datas e horários em ISO 8601;
- autenticação obrigatória quando aplicável;
- respostas HTTP coerentes;
- validação no backend;
- paginação em listagens extensas;
- mensagens de erro sem exposição de dados sensíveis.
""")

write("docs/05-api/padroes-resposta.md", """
# Padrões de Resposta da API

## Sucesso

```json
{
  "data": {
    "id": 1
  }
}
```

## Listagem

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 0
  }
}
```

## Erro de validação

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos.",
    "details": []
  }
}
```

## Códigos HTTP sugeridos

| Código | Uso |
| --- | --- |
| 200 | Consulta/alteração concluída |
| 201 | Recurso criado |
| 204 | Operação sem corpo de resposta |
| 400 | Requisição inválida |
| 401 | Não autenticado |
| 403 | Sem autorização |
| 404 | Recurso não encontrado |
| 409 | Conflito ou duplicidade |
| 422 | Regra de negócio/validação |
| 500 | Erro interno |

## Idempotência RFID

O reenvio do mesmo `event_id` não deverá produzir uma nova batida.

A API deverá responder de maneira que o terminal consiga considerar o evento
sincronizado mesmo quando ele já tiver sido recebido anteriormente.
""")

write("docs/05-api/autenticacao-autorizacao.md", """
# Autenticação e Autorização

## Perfis iniciais

### COORDENADOR
Administra os recursos do laboratório e analisa pendências.

### PARTICIPANTE
Consulta os próprios dados, registra atividades, envia relatórios,
justificativas e solicitações de ajuste.

## Terminal RFID

O terminal não utiliza credenciais de usuário.

Cada terminal deverá possuir uma credencial própria. O servidor armazena
somente uma representação segura dessa credencial.

## Princípios

- senha nunca armazenada em texto puro;
- autorização validada no backend;
- participante não acessa dados individuais de terceiros;
- operações administrativas relevantes são auditadas;
- credenciais e segredos não são versionados no Git.
""")

write("docs/02-requisitos/casos-de-uso.md", """
# Casos de Uso — CheckPonto

## UC01 — Autenticar usuário
**Ator:** Coordenador ou Participante.

**Fluxo:** informa credenciais, sistema valida e inicia sessão.

## UC02 — Cadastrar participante
**Ator:** Coordenador.

O coordenador cria a conta e os dados do participante.

## UC03 — Criar vínculo
**Ator:** Coordenador.

Associa participante, laboratório, tipo de vínculo, período e carga semanal.

## UC04 — Definir programação semanal
**Ator:** Coordenador.

Define dias, horários e carga prevista do vínculo.

## UC05 — Registrar cartão RFID
**Ator:** Coordenador.

Cadastra e atribui cartão ao participante.

## UC06 — Registrar evento RFID
**Ator:** Terminal RFID.

1. cartão é aproximado;
2. terminal lê UID;
3. gera `event_id`;
4. registra timestamp;
5. transmite evento;
6. servidor valida terminal;
7. evento bruto é armazenado;
8. servidor interpreta a batida;
9. jornada é recalculada.

## UC07 — Sincronizar evento offline
**Ator:** Terminal RFID.

Na ausência de rede, o evento permanece localmente e é retransmitido depois.
O `event_id` impede duplicação.

## UC08 — Consultar frequência
**Ator:** Participante.

Consulta registros, jornadas, carga prevista, realizada e saldo.

## UC09 — Registrar atividade diária
**Ator:** Participante.

Registra a descrição do trabalho. As horas são provenientes da jornada e não
digitadas manualmente.

## UC10 — Solicitar ajuste de ponto
**Ator:** Participante.

Informa registro/data, horário solicitado e justificativa.

## UC11 — Analisar ajuste
**Ator:** Coordenador.

Aprova ou rejeita sem apagar o evento RFID original.

## UC12 — Justificar ausência
**Ator:** Participante.

Apresenta justificativa referente à ausência.

## UC13 — Analisar justificativa
**Ator:** Coordenador.

Aprova ou rejeita e registra a decisão.

## UC14 — Registrar evento de calendário
**Ator:** Coordenador.

Registra feriado, recesso ou suspensão.

## UC15 — Registrar afastamento
**Ator:** Coordenador.

Registra período individual em que o participante não deverá gerar ausência.

## UC16 — Preencher resumo semanal
**Ator:** Participante.

Preenche o resumo das atividades do período.

## UC17 — Enviar relatório semanal
**Ator:** Participante.

Altera o relatório de EM_PREENCHIMENTO para ENVIADO.

## UC18 — Avaliar relatório semanal
**Ator:** Coordenador.

Pode APROVAR ou DEVOLVER com observação.

## UC19 — Corrigir relatório devolvido
**Ator:** Participante.

Corrige o conteúdo permitido e reenvia.

## UC20 — Consultar dashboard administrativo
**Ator:** Coordenador.

Visualiza presença, cargas, pendências, ocorrências e relatórios aguardando
análise.
""")

write("docs/03-arquitetura/fluxos-sistema.md", """
# Fluxos Principais

## Registro de ponto

```text
Cartão
  |
  v
RC522
  |
  v
ESP32
  |
  | UID + event_id + timestamp
  v
API
  |
  +--> autentica terminal
  +--> valida payload
  +--> verifica idempotência
  +--> salva EVENTO_RFID
  +--> identifica cartão/vínculo
  +--> interpreta sequência
  +--> atualiza REGISTRO_PONTO
  +--> recalcula JORNADA_DIARIA
  |
  v
Dashboard
```

## Atividade diária

```text
Participante
   |
   v
Login -> Jornada do dia -> Descrição da atividade -> Salvar
                              |
                              +-> horas vêm do ponto
```

## Relatório semanal

```text
Jornadas + Atividades + Ocorrências
              |
              v
       Consolidação semanal
              |
              v
       EM_PREENCHIMENTO
              |
        participante envia
              v
            ENVIADO
           /       \
     coordenador   coordenador
       aprova       devolve
         |             |
         v             v
     APROVADO      DEVOLVIDO
                       |
                    correção
                       |
                       v
                    ENVIADO
```

## Reinterpretação

Uma sequência pode inicialmente parecer:

```text
08:00 -> ENTRADA
12:00 -> SAIDA
```

Com um novo evento:

```text
13:00
```

o servidor poderá reinterpretar:

```text
08:00 -> ENTRADA
12:00 -> SAIDA_INTERVALO
13:00 -> RETORNO_INTERVALO
```

O EVENTO_RFID original permanece inalterado.
""")

write("docs/05-api/README.md", """
# API — Documentação Inicial

Esta pasta contém a especificação que servirá de referência para a equipe de
backend, frontend e firmware.

## Arquivos

- `endpoints.md` — recursos e endpoints planejados;
- `padroes-resposta.md` — formato das respostas e erros;
- `autenticacao-autorizacao.md` — perfis e princípios de segurança;
- `protocolo-rfid.md` — contrato do terminal RFID.

## Regra para os alunos

Antes de implementar ou alterar um endpoint:

1. consultar os requisitos relacionados;
2. verificar o modelo de dados;
3. verificar os casos de uso;
4. implementar;
5. testar;
6. atualizar esta documentação se o contrato mudar.

A documentação e o código devem evoluir juntos.
""")

print()
print("=" * 76)
print(" VALIDACAO")
print("=" * 76)

files = [
    "docs/05-api/endpoints.md",
    "docs/05-api/padroes-resposta.md",
    "docs/05-api/autenticacao-autorizacao.md",
    "docs/05-api/README.md",
    "docs/02-requisitos/casos-de-uso.md",
    "docs/03-arquitetura/fluxos-sistema.md",
]
errors = 0
for rel in files:
    p = ROOT / rel
    if p.exists() and p.stat().st_size > 0:
        print(f"[OK] {rel}")
    else:
        print(f"[ERRO] {rel}")
        errors += 1

uc = (ROOT / "docs/02-requisitos/casos-de-uso.md").read_text(encoding="utf-8")
count = sum(1 for i in range(1, 21) if f"UC{i:02d}" in uc)
print(f"[{'OK' if count == 20 else 'ERRO'}] Casos de uso: {count}/20")
if count != 20:
    errors += 1

if errors:
    print(f"[ERRO] Finalizado com {errors} problema(s).")
    sys.exit(1)

print("=" * 76)
print(" DOCUMENTACAO DE API E CASOS DE USO CONCLUIDA")
print("=" * 76)
print("Casos de uso: 20")
print("Nenhum servico foi instalado ou executado.")
print("Proxima etapa documental: hardware, testes e guia de desenvolvimento.")
