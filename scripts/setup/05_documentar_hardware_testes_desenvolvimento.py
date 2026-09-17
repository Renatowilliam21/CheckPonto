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
print(" CHECKPONTO - SCRIPT 05 - HARDWARE, TESTES E GUIA DE DESENVOLVIMENTO")
print("=" * 78)

for d in [
    "docs/06-hardware",
    "docs/07-testes",
    "docs/03-arquitetura",
    "firmware/esp32-rfid-terminal",
    ".github"
]:
    if not (ROOT / d).exists():
        fail(f"Execute na raiz do CheckPonto. Ausente: {d}")

# ------------------------------------------------------------------
# HARDWARE
# ------------------------------------------------------------------

write("docs/06-hardware/componentes.md", """
# Componentes de Hardware — CheckPonto

## Objetivo do terminal

O terminal RFID registra eventos físicos de aproximação de cartão e os envia
para a API do CheckPonto.

O terminal não deve decidir regras complexas de jornada.

## Componentes previstos

### ESP32

Microcontrolador responsável por:

- conexão Wi-Fi;
- leitura do RFID;
- geração do identificador do evento;
- obtenção de data/hora;
- envio para API;
- feedback ao usuário;
- armazenamento temporário offline.

### RC522

Leitor RFID utilizado para obter o UID do cartão.

### Cartões ou tags RFID

Identificadores físicos dos participantes.

### LEDs

Feedback simples:

- leitura detectada;
- sucesso;
- erro;
- operação offline.

### Buzzer

Feedback sonoro opcional.

### Display OLED

Componente opcional para apresentar mensagens como:

- cartão lido;
- registro recebido;
- sem conexão;
- sincronizando.

### RTC DS3231

Componente recomendado para manter referência temporal quando o terminal
estiver temporariamente sem acesso à rede.

## Observação

A lista é uma proposta de referência. A equipe de hardware deverá confirmar
os componentes disponíveis antes de fixar pinagem e montagem definitiva.
""")

write("docs/06-hardware/pinagem.md", """
# Pinagem — Terminal RFID

## Situação

A pinagem definitiva ainda não está congelada.

Isso é intencional: os alunos devem confirmar o modelo exato da placa ESP32,
do RC522 e dos componentes adicionais disponíveis no laboratório.

## RC522

O RC522 normalmente será utilizado via SPI.

Sinais necessários:

| Sinal | Função |
| --- | --- |
| SDA/SS | seleção SPI |
| SCK | clock |
| MOSI | dados ESP32 -> RC522 |
| MISO | dados RC522 -> ESP32 |
| RST | reset |
| 3.3V | alimentação |
| GND | terra |

## Regra importante

O RC522 deve operar com alimentação e níveis lógicos adequados ao módulo.
A montagem deverá ser conferida antes da energização.

## Antes de definir GPIOs

A equipe deverá:

1. identificar o modelo exato do ESP32;
2. verificar GPIOs reservados ou problemáticos;
3. verificar SPI disponível;
4. considerar OLED, buzzer, LEDs e RTC;
5. documentar a decisão;
6. atualizar esta página.

Não copiar pinagem de outro projeto sem conferir a placa utilizada.
""")

write("docs/06-hardware/montagem.md", """
# Montagem do Terminal

## Etapa 1 — Protótipo mínimo

Montar somente:

```text
ESP32 <-> RC522
```

Objetivo: ler o UID de cartões de forma confiável.

## Etapa 2 — Comunicação

Adicionar Wi-Fi e testar envio de um evento simulado para a API.

## Etapa 3 — Feedback

Adicionar LEDs, buzzer e/ou OLED conforme disponibilidade.

## Etapa 4 — Tempo

Adicionar estratégia de sincronização de relógio e, se adotado, RTC DS3231.

## Etapa 5 — Operação offline

Implementar fila local de eventos pendentes.

## Etapa 6 — Integração

Executar o fluxo:

```text
Cartão -> RC522 -> ESP32 -> API -> Banco -> Dashboard
```

## Critério de aceitação do protótipo

O terminal deve conseguir:

- identificar cartão;
- gerar evento único;
- registrar timestamp;
- enviar evento;
- reconhecer confirmação;
- não perder evento em falha temporária de rede;
- retransmitir sem duplicar o registro no servidor.
""")

write("docs/06-hardware/firmware.md", """
# Responsabilidades do Firmware

## Deve fazer

- inicializar componentes;
- conectar ao Wi-Fi;
- ler UID;
- normalizar UID;
- gerar `event_id`;
- obter timestamp;
- montar JSON;
- transmitir evento;
- interpretar resposta HTTP;
- fornecer feedback;
- enfileirar eventos offline;
- tentar sincronização posterior.

## Não deve fazer

O firmware não deve decidir:

- se uma batida é entrada ou saída;
- quantidade semanal obrigatória;
- aprovação de justificativa;
- saldo semanal;
- situação do relatório;
- regras administrativas.

## Evento mínimo

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

## Idempotência

O `event_id` precisa permanecer o mesmo durante retransmissões do mesmo
evento.

Gerar um novo ID em cada tentativa destruiria a proteção contra duplicidade.

## Organização sugerida do firmware

```text
src/
  main.cpp

include/
  config.h
  rfid_reader.h
  network.h
  event_queue.h
  api_client.h
  feedback.h
  clock_service.h
```

A divisão final poderá ser refinada pela equipe.
""")

# ------------------------------------------------------------------
# TESTES
# ------------------------------------------------------------------

write("docs/07-testes/plano-testes.md", """
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
""")

write("docs/07-testes/casos-testes.md", """
# Casos de Teste Iniciais

## CT01 — Jornada simples

Eventos:

```text
08:00 ENTRADA
12:00 SAIDA
```

Esperado: 240 minutos realizados.

## CT02 — Jornada com almoço

```text
08:00 ENTRADA
12:00 SAIDA_INTERVALO
13:00 RETORNO_INTERVALO
17:00 SAIDA
```

Esperado: 480 minutos realizados.

## CT03 — Intervalo não contabilizado

Entre 12:00 e 13:00 não deve haver acréscimo à carga.

## CT04 — Evento duplicado

Enviar duas vezes o mesmo `event_id`.

Esperado: apenas um EVENTO_RFID.

## CT05 — Cartão desconhecido

Esperado: evento preservado como não reconhecido e nenhum ponto atribuído a
participante incorreto.

## CT06 — Jornada incompleta

```text
08:00 ENTRADA
```

Esperado: ocorrência de ponto.

## CT07 — Reinterpretação

Receber:

```text
08:00
12:00
```

Depois receber:

```text
13:00
17:00
```

Esperado: sequência final coerente com intervalo, preservando eventos brutos.

## CT08 — Bolsista com 16 horas

Programação semanal total: 960 minutos.

Realizado: 960.

Esperado: saldo 0.

## CT09 — Carga abaixo da prevista

Previsto: 960.

Realizado: 840.

Esperado: saldo -120 minutos.

## CT10 — Feriado

Dia programado marcado como feriado.

Esperado: não gerar falta automática.

## CT11 — Recesso

Período programado marcado como recesso.

Esperado: não gerar carga pendente automática.

## CT12 — Afastamento

Participante afastado no período.

Esperado: não gerar falta automática durante o afastamento.

## CT13 — Solicitação de ajuste

Participante solicita correção.

Esperado: registro original preservado e solicitação PENDENTE.

## CT14 — Ajuste aprovado

Esperado: correção aplicada de forma rastreável.

## CT15 — Ajuste rejeitado

Esperado: ponto original permanece válido e decisão é registrada.

## CT16 — Atividade sem horas manuais

Participante registra descrição.

Esperado: horas exibidas vêm da jornada.

## CT17 — Envio de relatório

EM_PREENCHIMENTO -> ENVIADO.

## CT18 — Aprovação

ENVIADO -> APROVADO.

## CT19 — Devolução

ENVIADO -> DEVOLVIDO.

## CT20 — Reenvio

DEVOLVIDO -> correção -> ENVIADO.

## CT21 — Permissão do participante

Participante tenta acessar dados privados de outro participante.

Esperado: acesso negado.

## CT22 — Terminal sem rede

Evento é armazenado localmente.

Esperado: evento não é perdido.

## CT23 — Retorno da rede

Eventos pendentes são sincronizados.

Esperado: todos chegam uma única vez ao servidor.

## CT24 — Cartão bloqueado

Esperado: não gerar ponto válido.

## CT25 — Histórico de programação

Alterar programação.

Esperado: programação anterior permanece disponível historicamente.
""")

write("docs/07-testes/matriz-rastreabilidade.md", """
# Matriz de Rastreabilidade

A equipe deverá manter relação entre requisito, caso de uso, implementação e
teste.

Modelo:

| Requisito | Caso de uso | Módulo | Teste |
| --- | --- | --- | --- |
| RF17 | UC06 | Firmware/API | CT04 |
| RF20 | UC07 | Firmware/API | CT22, CT23 |
| RF29 | UC06 | Backend | CT01, CT02 |
| RF30 | UC06 | Backend | CT03 |
| RF34 | UC10 | Backend/Frontend | CT13 |
| RF36 | UC11 | Backend/Frontend | CT14, CT15 |
| RF41 | UC14 | Backend | CT10 |
| RF43 | UC15 | Backend | CT12 |
| RF45 | UC09 | Backend/Frontend | CT16 |
| RF54 | UC17 | Backend/Frontend | CT17 |
| RF55 | UC18 | Backend/Frontend | CT18 |
| RF56 | UC18 | Backend/Frontend | CT19 |

A matriz deverá ser expandida conforme o desenvolvimento.
""")

# ------------------------------------------------------------------
# GUIA DOS ALUNOS
# ------------------------------------------------------------------

write("docs/09-desenvolvimento/guia-alunos.md", """
# Guia de Desenvolvimento para os Alunos

## 1. Antes de programar

Todos devem conhecer:

1. `README.md`;
2. `docs/01-visao/`;
3. `docs/02-requisitos/`;
4. `docs/03-arquitetura/`;
5. documentação do módulo em que trabalharão.

Não iniciar pela criação de telas sem compreender o fluxo de negócio.

## 2. Organização técnica

```text
frontend/       aplicação web
backend/        API e regras de negócio
database/       banco e modelo
firmware/       ESP32/RFID
infrastructure/ infraestrutura
tests/          testes globais
docs/           documentação
```

## 3. Fluxo de trabalho

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

## 4. Branches

Exemplos:

```text
feature/login
feature/cadastro-participante
feature/programacao-semanal
feature/leitura-rfid
feature/registro-atividade
fix/evento-rfid-duplicado
docs/protocolo-rfid
```

Não desenvolver diretamente na `main`.

## 5. Commits

Padrão sugerido:

```text
feat: adiciona cadastro de participantes
fix: corrige calculo da jornada diaria
docs: atualiza protocolo RFID
test: adiciona teste de evento duplicado
refactor: reorganiza servico de ponto
chore: ajusta configuracao do projeto
```

## 6. Pull Request

O PR deve informar:

- o que foi desenvolvido;
- requisito relacionado;
- como testar;
- evidências quando aplicável;
- limitações conhecidas.

## 7. Definição de pronto

Uma tarefa está pronta quando:

- atende ao requisito;
- respeita a arquitetura;
- possui validações;
- possui tratamento básico de erro;
- foi testada;
- não contém segredos;
- documentação afetada foi atualizada;
- passou por revisão.

## 8. Regra importante

O projeto deve crescer incrementalmente.

Evitar implementar muitos módulos incompletos ao mesmo tempo.
""")

write("docs/09-desenvolvimento/divisao-modulos.md", """
# Divisão Inicial dos Módulos

A divisão abaixo é uma referência. O professor poderá ajustar conforme o
número de alunos.

## Módulo A — Base e acesso

Responsabilidades:

- autenticação;
- usuários;
- perfis;
- laboratórios;
- participantes;
- vínculos.

## Módulo B — Programação e frequência

Responsabilidades:

- programação semanal;
- eventos RFID;
- registros de ponto;
- interpretação;
- jornadas;
- ocorrências.

## Módulo C — Atividades e relatórios

Responsabilidades:

- atividades diárias;
- resumo semanal;
- relatório semanal;
- aprovação/devolução;
- relatórios por período.

## Módulo D — Ocorrências administrativas

Responsabilidades:

- justificativas;
- ajustes;
- calendário;
- afastamentos;
- auditoria.

## Módulo E — Terminal RFID

Responsabilidades:

- ESP32;
- RC522;
- Wi-Fi;
- protocolo;
- feedback;
- fila offline;
- sincronização.

## Integração

As equipes não devem trabalhar como projetos isolados.

Toda funcionalidade deve respeitar o contrato comum da API e o modelo de
dados.
""")

write("docs/09-desenvolvimento/roteiro-3-meses.md", """
# Roteiro de Desenvolvimento — 3 Meses

## Mês 1 — Fundação

### Semana 1
- leitura da documentação;
- apresentação do domínio;
- organização das equipes;
- Git/GitHub;
- Issues iniciais.

### Semana 2
- estrutura inicial frontend/backend;
- banco de desenvolvimento;
- autenticação;
- usuários;
- laboratórios.

### Semana 3
- participantes;
- vínculos;
- projetos;
- cartões;
- terminais.

### Semana 4
- programação semanal;
- protótipo ESP32 + RC522;
- primeiros testes de integração.

## Mês 2 — Núcleo

### Semana 5
- ingestão RFID;
- idempotência;
- registros de ponto.

### Semana 6
- interpretação de batidas;
- jornada diária;
- carga semanal.

### Semana 7
- atividades diárias;
- dashboard do participante;
- ocorrências.

### Semana 8
- justificativas;
- ajustes;
- calendário;
- afastamentos.

## Mês 3 — Consolidação

### Semana 9
- relatório semanal;
- envio;
- aprovação;
- devolução.

### Semana 10
- dashboard do coordenador;
- relatórios por período.

### Semana 11
- fila offline do terminal;
- integração ponta a ponta;
- testes.

### Semana 12
- correções;
- documentação;
- demonstração;
- fechamento da versão MVP.

## Regra

O cronograma é incremental. Uma semana pode ser ajustada conforme a evolução
real das equipes.
""")

write("docs/09-desenvolvimento/backlog-inicial.md", """
# Backlog Inicial

## Épico 1 — Acesso
- autenticação;
- perfil coordenador;
- perfil participante.

## Épico 2 — Cadastros
- laboratórios;
- participantes;
- tipos de vínculo;
- vínculos;
- projetos;
- cartões;
- terminais.

## Épico 3 — Programação
- programação semanal;
- programação por dia;
- histórico.

## Épico 4 — RFID
- leitura;
- evento único;
- envio;
- autenticação do terminal;
- idempotência;
- fila offline.

## Épico 5 — Ponto
- evento bruto;
- interpretação;
- jornada;
- intervalo;
- ocorrência;
- saldo.

## Épico 6 — Atividades
- atividade diária;
- associação com projeto;
- consulta semanal.

## Épico 7 — Ocorrências administrativas
- justificativa;
- ajuste;
- calendário;
- afastamento.

## Épico 8 — Relatório semanal
- consolidação;
- resumo;
- envio;
- aprovação;
- devolução.

## Épico 9 — Dashboards
- participante;
- coordenador;
- presentes;
- pendências.

## Épico 10 — Qualidade
- testes;
- documentação;
- auditoria;
- integração;
- revisão final.
""")

write("docs/09-desenvolvimento/README.md", """
# Desenvolvimento

Documentos para orientar as equipes:

- `guia-alunos.md` — regras gerais de trabalho;
- `divisao-modulos.md` — módulos do sistema;
- `roteiro-3-meses.md` — sequência sugerida;
- `backlog-inicial.md` — épicos iniciais.

Esses documentos orientam o início do projeto, mas não substituem Issues,
Pull Requests e documentação técnica de cada módulo.
""")

# ------------------------------------------------------------------
# README FIRMWARE
# ------------------------------------------------------------------

write("firmware/esp32-rfid-terminal/README.md", """
# Terminal RFID — CheckPonto

Firmware do terminal físico do sistema.

## Responsabilidade

```text
Cartão -> RC522 -> ESP32 -> API
```

O firmware coleta o fato físico e transmite o evento.

As regras de jornada permanecem no backend.

## Desenvolvimento sugerido

1. leitura do UID;
2. Wi-Fi;
3. geração de event_id;
4. timestamp;
5. JSON;
6. envio HTTP;
7. feedback;
8. fila offline;
9. sincronização;
10. testes de integração.

Consultar:

- `docs/06-hardware/componentes.md`;
- `docs/06-hardware/pinagem.md`;
- `docs/06-hardware/montagem.md`;
- `docs/06-hardware/firmware.md`;
- `docs/05-api/protocolo-rfid.md`.
""")

# ------------------------------------------------------------------
# CONTRIBUIÇÃO
# ------------------------------------------------------------------

write("CONTRIBUTING.md", """
# Como Contribuir com o CheckPonto

## Fluxo

1. selecionar uma Issue;
2. criar branch;
3. desenvolver;
4. testar;
5. atualizar documentação quando necessário;
6. realizar commits claros;
7. enviar branch;
8. abrir Pull Request;
9. corrigir observações da revisão;
10. integrar somente após aprovação.

## Branch

Não trabalhar diretamente na `main`.

## Commits

Use mensagens objetivas, por exemplo:

```text
feat: adiciona cadastro de participantes
fix: evita duplicidade de evento RFID
docs: atualiza fluxo de jornada
test: adiciona teste de intervalo
```

## Pull Requests

Todo PR deve indicar requisito, mudança realizada e forma de teste.

## Segurança

Nunca versionar:

- senhas;
- tokens;
- chaves de API;
- credenciais de banco;
- arquivos `.env` reais.

## Documentação

Mudanças no comportamento do sistema devem atualizar a documentação
correspondente.
""")

# ------------------------------------------------------------------
# VALIDAÇÃO
# ------------------------------------------------------------------

print()
print("=" * 78)
print(" VALIDACAO")
print("=" * 78)

files = [
    "docs/06-hardware/componentes.md",
    "docs/06-hardware/pinagem.md",
    "docs/06-hardware/montagem.md",
    "docs/06-hardware/firmware.md",
    "docs/07-testes/plano-testes.md",
    "docs/07-testes/casos-testes.md",
    "docs/07-testes/matriz-rastreabilidade.md",
    "docs/09-desenvolvimento/guia-alunos.md",
    "docs/09-desenvolvimento/divisao-modulos.md",
    "docs/09-desenvolvimento/roteiro-3-meses.md",
    "docs/09-desenvolvimento/backlog-inicial.md",
    "docs/09-desenvolvimento/README.md",
    "firmware/esp32-rfid-terminal/README.md",
    "CONTRIBUTING.md",
]

errors = 0
for rel in files:
    p = ROOT / rel
    if p.exists() and p.stat().st_size > 0:
        print(f"[OK] {rel}")
    else:
        print(f"[ERRO] {rel}")
        errors += 1

tests = (ROOT / "docs/07-testes/casos-testes.md").read_text(encoding="utf-8")
test_count = sum(1 for i in range(1, 26) if f"CT{i:02d}" in tests)

print(f"[{'OK' if test_count == 25 else 'ERRO'}] Casos de teste: {test_count}/25")
if test_count != 25:
    errors += 1

if errors:
    print(f"[ERRO] Finalizado com {errors} problema(s).")
    sys.exit(1)

print()
print("=" * 78)
print(" BASE PEDAGOGICA DE DESENVOLVIMENTO CONFIGURADA COM SUCESSO")
print("=" * 78)
print("Casos de teste iniciais: 25")
print("Nenhum servico foi instalado ou executado.")
print("Proxima etapa: revisar a documentacao geral e preparar o indice do projeto.")
