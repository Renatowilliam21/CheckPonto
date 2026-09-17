from pathlib import Path
import sys

ROOT = Path.cwd()
BASE = ROOT / "docs" / "09-desenvolvimento" / "issues"

def fail(msg):
    print(f"[ERRO] {msg}")
    sys.exit(1)

def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"[OK] {rel} ({p.stat().st_size} bytes)")

print("=" * 78)
print(" CHECKPONTO - SCRIPT 07 - ISSUES INICIAIS DE DESENVOLVIMENTO")
print("=" * 78)

required = [
    "docs/02-requisitos/requisitos-funcionais.md",
    "docs/02-requisitos/regras-negocio.md",
    "docs/02-requisitos/casos-de-uso.md",
    "docs/07-testes/casos-testes.md",
    "docs/09-desenvolvimento/roteiro-3-meses.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"Documentacao necessaria ausente: {rel}")

issues = [
("01-backend-base.md", """
# Issue 01 — [BASE] Estruturar aplicação backend Node.js + TypeScript

## Objetivo
Criar a fundação técnica da API REST do CheckPonto.

## Escopo
- iniciar projeto Node.js + TypeScript em `backend/`;
- organizar `routes`, `controllers`, `services`, `repositories`, `validators` e `middlewares`;
- configurar variáveis de ambiente;
- preparar acesso ao PostgreSQL;
- criar endpoint de health check;
- documentar execução local.

## Referências
- RNF02, RNF03, RNF05, RNF10, RNF12
- `docs/03-arquitetura/`
- `docs/05-api/`

## Critérios de aceitação
- [ ] backend inicia sem erros;
- [ ] TypeScript configurado;
- [ ] estrutura segue a arquitetura;
- [ ] endpoint de saúde disponível;
- [ ] nenhuma credencial real versionada;
- [ ] README do backend atualizado;
- [ ] alteração enviada por Pull Request.

## Testes esperados
- inicialização da aplicação;
- resposta do health check;
- tratamento de configuração ausente.

## Dependências
Nenhuma.

## Fora do escopo
Autenticação e regras de negócio.
"""),
("02-frontend-base.md", """
# Issue 02 — [BASE] Estruturar aplicação frontend React + TypeScript

## Objetivo
Criar a fundação da interface web do CheckPonto.

## Escopo
- iniciar React + TypeScript + Vite em `frontend/`;
- criar estrutura de páginas, componentes, serviços e rotas;
- criar layout base;
- preparar cliente HTTP;
- utilizar o mockup apenas como referência visual inicial.

## Referências
- RNF01, RNF05, RNF12
- `docs/10-mockups/`
- `docs/05-api/`

## Critérios de aceitação
- [ ] frontend inicia sem erros;
- [ ] navegação base preparada;
- [ ] componentes organizados;
- [ ] configuração da URL da API via ambiente;
- [ ] layout responsivo inicial;
- [ ] README atualizado.

## Testes esperados
- inicialização;
- renderização da página inicial;
- navegação básica.

## Dependências
Nenhuma.

## Fora do escopo
Implementação completa das telas de negócio.
"""),
("03-autenticacao.md", """
# Issue 03 — [AUTH] Implementar autenticação e perfis

## Objetivo
Permitir acesso autenticado de coordenadores e participantes.

## Escopo
- login por usuário/senha;
- armazenamento seguro de senha;
- sessão/token;
- middleware de autenticação;
- autorização por perfil;
- endpoint `/auth/me`;
- tela de login.

## Requisitos relacionados
- RF01, RF03, RF04, RF05
- RNF03, RNF05
- UC01
- CT21

## Critérios de aceitação
- [ ] credenciais válidas autenticam;
- [ ] credenciais inválidas são rejeitadas;
- [ ] senha não fica em texto puro;
- [ ] rotas protegidas exigem autenticação;
- [ ] participante não acessa dados privados de terceiros;
- [ ] frontend trata sessão e logout.

## Dependências
- Issue 01
- Issue 02

## Testes esperados
Login válido, login inválido, rota sem token e permissão por perfil.
"""),
("04-laboratorios.md", """
# Issue 04 — [CADASTRO] Implementar gestão de laboratórios

## Objetivo
Permitir ao coordenador cadastrar e manter laboratórios.

## Requisitos relacionados
- RF06, RF07
- RN01
- UC02/UC03 como contexto administrativo

## Escopo
- listar;
- cadastrar;
- consultar;
- atualizar;
- associar coordenador ao laboratório;
- interface correspondente.

## Critérios de aceitação
- [ ] CRUD previsto funciona;
- [ ] validações impedem dados inválidos;
- [ ] associação de coordenador funciona;
- [ ] acesso administrativo é protegido;
- [ ] interface apresenta feedback de sucesso/erro.

## Dependências
Issues 01, 02 e 03.

## Testes esperados
Cadastro válido, validação, consulta, atualização e autorização.
"""),
("05-participantes.md", """
# Issue 05 — [CADASTRO] Implementar gestão de participantes

## Objetivo
Cadastrar e consultar bolsistas e estagiários que utilizarão o sistema.

## Requisitos relacionados
- RF02, RF03, RF04, RF05
- UC02
- RN01

## Escopo
- cadastro;
- listagem;
- consulta;
- atualização;
- ativação/desativação;
- vínculo com conta de usuário.

## Critérios de aceitação
- [ ] coordenador cadastra participante;
- [ ] dados obrigatórios são validados;
- [ ] participante pode ser desativado sem apagar histórico;
- [ ] participante consulta apenas seus próprios dados permitidos;
- [ ] tela segue padrões do projeto.

## Dependências
Issues 01, 02 e 03.

## Testes esperados
Cadastro, duplicidade relevante, atualização, desativação e autorização.
"""),
("06-vinculos.md", """
# Issue 06 — [CADASTRO] Implementar vínculos de bolsistas e estagiários

## Objetivo
Associar participantes a laboratórios e tipos de vínculo.

## Requisitos relacionados
- RF10, RF11
- RN01, RN03, RN04, RN05, RN06, RN07
- UC03
- CT08, CT09

## Escopo
- tipos de vínculo;
- criação do vínculo;
- laboratório;
- período;
- carga semanal;
- encerramento;
- preservação do histórico.

## Critérios de aceitação
- [ ] BOLSISTA e ESTAGIARIO disponíveis;
- [ ] vínculo registra período e laboratório;
- [ ] carga é configurável;
- [ ] encerramento não apaga histórico;
- [ ] bolsista pode utilizar referência de 16h/semana.

## Dependências
Issues 04 e 05.

## Testes esperados
Criação, período inválido, encerramento e consulta histórica.
"""),
("07-projetos.md", """
# Issue 07 — [CADASTRO] Implementar gestão de projetos

## Objetivo
Permitir cadastro de projetos/atividades e associação de participantes.

## Requisitos relacionados
- RF08, RF09

## Escopo
- listar projetos;
- cadastrar;
- consultar;
- atualizar;
- associar/desassociar participantes preservando coerência histórica.

## Critérios de aceitação
- [ ] CRUD de projeto disponível;
- [ ] participante pode ser associado;
- [ ] consultas exibem participantes associados;
- [ ] operações administrativas são protegidas.

## Dependências
Issues 03 e 05.

## Testes esperados
Cadastro, atualização, associação e autorização.
"""),
("08-cartoes-rfid.md", """
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
"""),
("09-terminais.md", """
# Issue 09 — [RFID] Implementar cadastro e autenticação de terminais

## Objetivo
Permitir que somente terminais autorizados enviem eventos RFID.

## Requisitos relacionados
- RF15, RF17
- RNF04
- UC06

## Escopo
- cadastrar terminal;
- identificar `device_id`;
- gerar/administrar credencial;
- armazenar somente representação segura da credencial;
- autenticar requisições do terminal.

## Critérios de aceitação
- [ ] terminal cadastrado possui identificador único;
- [ ] terminal autorizado envia requisição;
- [ ] terminal não autorizado é rejeitado;
- [ ] segredo não é armazenado em texto puro quando aplicável;
- [ ] logs não expõem segredo.

## Dependências
Issue 01.

## Testes esperados
Terminal válido, inválido e credencial ausente.
"""),
("10-programacao-semanal.md", """
# Issue 10 — [FREQUÊNCIA] Implementar programação semanal individual

## Objetivo
Permitir ao coordenador definir a carga planejada de cada vínculo.

## Requisitos relacionados
- RF21, RF22, RF23, RF24, RF25
- RN04, RN05, RN06, RN07, RN18
- UC04
- CT08, CT09, CT25

## Escopo
- programação por vínculo;
- dias da semana;
- horários;
- minutos previstos;
- vigência;
- cálculo semanal;
- histórico.

## Critérios de aceitação
- [ ] programação individual pode ser criada;
- [ ] total semanal é calculado;
- [ ] bolsista e estagiário podem ter configurações distintas;
- [ ] alteração não destrói programação anterior;
- [ ] interface permite visualizar programação vigente.

## Dependências
Issue 06.

## Testes esperados
Carga semanal, dias distintos, mudança de programação e histórico.
"""),
("11-prototipo-esp32-rc522.md", """
# Issue 11 — [HARDWARE] Criar protótipo ESP32 + RC522

## Objetivo
Obter leitura confiável de cartões RFID no terminal físico.

## Requisitos relacionados
- RF16, RF18
- UC06

## Referências
- `docs/06-hardware/`
- `firmware/esp32-rfid-terminal/README.md`

## Escopo
- confirmar placa ESP32;
- confirmar RC522;
- definir e documentar pinagem;
- montar protótipo;
- ler UID;
- normalizar UID;
- fornecer feedback básico.

## Critérios de aceitação
- [ ] pinagem real documentada;
- [ ] UID é lido repetidamente com estabilidade;
- [ ] diferentes cartões são distinguidos;
- [ ] firmware está organizado no repositório;
- [ ] montagem é documentada.

## Dependências
Nenhuma de software.

## Testes esperados
Leituras repetidas, cartões diferentes e ausência de cartão.

## Fora do escopo
Interpretação de entrada/saída.
"""),
("12-integracao-terminal-api.md", """
# Issue 12 — [INTEGRAÇÃO] Enviar evento RFID do terminal para a API

## Objetivo
Realizar a primeira integração ponta a ponta entre ESP32 e backend.

## Requisitos relacionados
- RF17, RF19, RF20, RF26
- RN08, RN09
- RNF02, RNF04, RNF07, RNF08, RNF09
- UC06, UC07
- CT04, CT05, CT22, CT23

## Evento de referência

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

## Escopo
- gerar `event_id`;
- obter timestamp;
- montar JSON;
- autenticar terminal;
- POST para API;
- armazenar EVENTO_RFID;
- impedir duplicidade;
- preparar comportamento para falha de rede.

## Critérios de aceitação
- [ ] evento válido chega ao backend;
- [ ] evento é persistido;
- [ ] mesmo `event_id` retransmitido não duplica;
- [ ] cartão desconhecido não é atribuído incorretamente;
- [ ] falha HTTP é tratada pelo firmware;
- [ ] terminal recebe confirmação adequada.

## Dependências
Issues 01, 08, 09 e 11.

## Testes esperados
CT04, CT05, CT22 e CT23.

## Fora do escopo
Interpretação completa da jornada, que será implementada em etapa posterior.
""")
]

for filename, content in issues:
    write(f"docs/09-desenvolvimento/issues/{filename}", content)

write("docs/09-desenvolvimento/issues/README.md", """
# Issues Iniciais — CheckPonto

Esta pasta contém as primeiras tarefas planejadas para o desenvolvimento.

## Ordem sugerida

| Nº | Issue | Pode iniciar |
| --- | --- | --- |
| 01 | Backend base | imediatamente |
| 02 | Frontend base | imediatamente |
| 03 | Autenticação | após bases |
| 04 | Laboratórios | após autenticação |
| 05 | Participantes | após autenticação |
| 06 | Vínculos | após laboratórios e participantes |
| 07 | Projetos | após participantes |
| 08 | Cartões RFID | após participantes |
| 09 | Terminais | após backend |
| 10 | Programação semanal | após vínculos |
| 11 | ESP32 + RC522 | imediatamente |
| 12 | Terminal -> API | após backend, cartões, terminais e protótipo |

## Trilhas paralelas

```text
SOFTWARE
01 Backend ----+----> 03 Auth ---> 04 Laboratórios ---+
               |                   05 Participantes ---+--> 06 Vínculos --> 10 Programação
               |                          |
               |                          +--> 07 Projetos
               |                          +--> 08 Cartões ----+
               +----------------> 09 Terminais ---------------+--> 12 Integração

HARDWARE
11 ESP32 + RC522 ----------------------------------------------> 12 Integração
```

## Uso

Cada arquivo pode ser copiado para uma Issue do GitHub quando a tarefa for
liberada para uma equipe.

O professor poderá acrescentar responsável, prazo, prioridade e observações
antes da abertura.

## Regra pedagógica

Não abrir uma tarefa dependente como atividade principal antes de sua base
estar disponível. Isso reduz retrabalho e conflitos entre equipes.
""")

# Atualiza índice de desenvolvimento sem apagar os documentos existentes.
readme = ROOT / "docs/09-desenvolvimento/README.md"
if readme.exists():
    current = readme.read_text(encoding="utf-8").rstrip()
else:
    current = "# Desenvolvimento"
addition = """

## Issues planejadas

As primeiras tarefas de implementação estão organizadas em:

[issues/README.md](issues/README.md)

Elas devem ser liberadas progressivamente conforme as dependências.
"""
if "issues/README.md" not in current:
    readme.write_text(current + addition + "\n", encoding="utf-8")
    print("[OK] docs/09-desenvolvimento/README.md atualizado")
else:
    print("[OK] docs/09-desenvolvimento/README.md ja referencia as Issues")

print()
print("=" * 78)
print(" VALIDACAO")
print("=" * 78)

errors = 0
for filename, _ in issues:
    p = BASE / filename
    if p.exists() and p.stat().st_size > 0:
        print(f"[OK] {filename}")
    else:
        print(f"[ERRO] {filename}")
        errors += 1

if (BASE / "README.md").exists():
    print("[OK] README das Issues")
else:
    print("[ERRO] README das Issues")
    errors += 1

print(f"Issues planejadas: {len(issues)}/12")

if errors:
    print(f"[ERRO] Finalizado com {errors} problema(s).")
    sys.exit(1)

print()
print("=" * 78)
print(" ISSUES INICIAIS DOCUMENTADAS COM SUCESSO")
print("=" * 78)
print("12 tarefas iniciais preparadas.")
print("Nenhuma Issue foi criada automaticamente no GitHub.")
print("Nenhum servico foi instalado ou executado.")
print("Proxima etapa: versionar este planejamento no repositorio.")
