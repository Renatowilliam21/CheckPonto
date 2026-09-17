from pathlib import Path
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
        fail(f"Falha ao gravar: {rel}")
    print(f"[OK] {rel} ({path.stat().st_size} bytes)")

print()
print("=" * 74)
print(" CHECKPONTO - SCRIPT 02 - MODELO LOGICO E BANCO DE DADOS")
print("=" * 74)
print()

required = [
    "docs/04-banco-dados",
    "database",
    "database/diagrams",
    "database/migrations",
    "database/seeds",
]
for rel in required:
    path = ROOT / rel
    if not path.exists():
        fail(f"Execute na raiz do CheckPonto. Ausente: {rel}")

print(f"[OK] Raiz: {ROOT}")
print()

write_file("docs/04-banco-dados/modelo-logico.md", """
# Modelo Lógico — CheckPonto

## 1. Objetivo

Este documento define o modelo lógico inicial do CheckPonto antes da criação
das migrations PostgreSQL.

O modelo foi estruturado para preservar histórico, permitir múltiplos
laboratórios e manter separados os eventos físicos de RFID, sua interpretação
como ponto e a consolidação da jornada.

## 2. Princípios

1. Eventos RFID são fatos brutos e imutáveis.
2. A interpretação do ponto pertence ao servidor.
3. Durações são armazenadas em minutos inteiros.
4. Datas e horários de eventos usam `TIMESTAMPTZ`.
5. Registros históricos não devem ser removidos por exclusões em cascata.
6. Cartões, usuários, terminais e vínculos são preferencialmente desativados.
7. Operações relevantes são auditáveis.
8. A ingestão RFID é idempotente por `event_uuid`.
9. O modelo suporta mais de um laboratório.
10. Regras de negócio não ficam embutidas no firmware.

## 3. Entidades

### usuario
Conta de autenticação.

### laboratorio
Unidade organizacional acompanhada pelo sistema.

### usuario_laboratorio
Associação entre coordenadores/usuários autorizados e laboratórios.

### participante
Dados específicos de uma pessoa que participa do controle de frequência.

### tipo_vinculo
Tipos de vínculo, inicialmente BOLSISTA e ESTAGIARIO.

### vinculo
Associa participante, laboratório e tipo de vínculo durante um período.

A associação com laboratório fica no vínculo para preservar histórico e
permitir que um participante possua vínculos em laboratórios diferentes ao
longo do tempo.

### projeto
Projeto desenvolvido em um laboratório.

### participante_projeto
Histórico da participação em projetos.

### cartao_rfid
Representa um cartão RFID físico.

### cartao_participante
Histórico de atribuição de cartões a participantes.

Isso evita perder rastreabilidade caso um cartão seja substituído ou
reutilizado no futuro.

### terminal
Terminal ESP32/RFID de um laboratório.

### programacao
Versão histórica da programação semanal de um vínculo.

### programacao_dia
Configuração de um dia da semana.

### evento_rfid
Evento bruto recebido do terminal.

Mesmo UIDs não reconhecidos podem ser registrados para diagnóstico e
auditoria.

### registro_ponto
Interpretação de um evento ou ajuste administrativo.

`evento_rfid_id` pode ser nulo porque um ajuste aprovado pode criar um
registro sem evento físico correspondente.

### ocorrencia_ponto
Representa inconsistências detectadas, como jornada incompleta ou sequência
inválida.

### jornada_diaria
Consolidação diária de carga prevista, realizada e saldo.

### atividade_diaria
Descrição das atividades realizadas pelo participante.

Não armazena carga horária manualmente editável.

### evento_calendario
Feriado, recesso ou suspensão associado ao laboratório.

### afastamento
Período individual de afastamento.

### justificativa
Justificativa apresentada pelo participante.

### solicitacao_ajuste
Pedido de correção de ponto.

### relatorio_semanal
Consolidação semanal submetida ao coordenador.

### auditoria
Histórico de alterações administrativas relevantes.

## 4. Relacionamentos principais

```text
USUARIO
  |
  +---- USUARIO_LABORATORIO ---- LABORATORIO
  |
  +---- PARTICIPANTE
             |
             +---- VINCULO ---- TIPO_VINCULO
             |       |
             |       +---- LABORATORIO
             |
             +---- CARTAO_PARTICIPANTE ---- CARTAO_RFID
             |
             +---- PARTICIPANTE_PROJETO ---- PROJETO
             |
             +---- JORNADA_DIARIA
             |        |
             |        +---- ATIVIDADE_DIARIA
             |
             +---- JUSTIFICATIVA
             +---- SOLICITACAO_AJUSTE
             +---- RELATORIO_SEMANAL

LABORATORIO
  |
  +---- TERMINAL ---- EVENTO_RFID
  |
  +---- PROJETO
  |
  +---- EVENTO_CALENDARIO

VINCULO
  |
  +---- PROGRAMACAO ---- PROGRAMACAO_DIA
  |
  +---- REGISTRO_PONTO
  |
  +---- OCORRENCIA_PONTO
```

## 5. Evento, interpretação e consolidação

O núcleo do controle de frequência possui três níveis:

```text
EVENTO_RFID
    |
    | interpretação
    v
REGISTRO_PONTO
    |
    | consolidação
    v
JORNADA_DIARIA
```

Um evento físico nunca deve ser sobrescrito para representar uma correção.

## 6. Política temporal

Eventos físicos e registros de ponto usarão `TIMESTAMPTZ`.

A apresentação para o usuário deverá utilizar o fuso de negócio configurado
pela aplicação. Inicialmente o projeto poderá utilizar `America/Fortaleza`.

Datas puramente administrativas, como início e fim de vínculo, usam `DATE`.

Durações usam minutos inteiros.

## 7. Política de exclusão

Dados históricos de frequência, jornadas, relatórios, justificativas,
ajustes e auditoria não devem ser excluídos automaticamente quando entidades
administrativas forem desativadas.

O padrão será preservar o histórico e utilizar campos como `ativo`,
`data_fim` ou `status`.
""")

write_file("docs/04-banco-dados/dicionario-dados.md", """
# Dicionário de Dados — CheckPonto

## usuario

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| nome | VARCHAR(150) | NOT NULL |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| senha_hash | VARCHAR(255) | NOT NULL |
| perfil | VARCHAR(30) | COORDENADOR ou PARTICIPANTE |
| ativo | BOOLEAN | default TRUE |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

## laboratorio

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| nome | VARCHAR(150) | NOT NULL |
| sigla | VARCHAR(30) | NOT NULL |
| descricao | TEXT | opcional |
| ativo | BOOLEAN | default TRUE |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

## usuario_laboratorio

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| usuario_id | BIGINT | FK usuario |
| laboratorio_id | BIGINT | FK laboratorio |
| papel | VARCHAR(30) | inicialmente COORDENADOR |
| ativo | BOOLEAN | default TRUE |
| created_at | TIMESTAMPTZ | NOT NULL |

Restrição única: `usuario_id + laboratorio_id + papel`.

## participante

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| usuario_id | BIGINT | FK usuario, UNIQUE |
| matricula | VARCHAR(80) | opcional |
| situacao | VARCHAR(30) | ATIVO, INATIVO, CONCLUIDO ou AFASTADO |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

## tipo_vinculo

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| nome | VARCHAR(80) | UNIQUE |
| carga_semanal_padrao_min | INTEGER | >= 0 |
| carga_diaria_minima_min | INTEGER | opcional, >= 0 |
| carga_diaria_maxima_min | INTEGER | opcional, >= mínima |
| ativo | BOOLEAN | default TRUE |

## vinculo

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| participante_id | BIGINT | FK participante |
| laboratorio_id | BIGINT | FK laboratorio |
| tipo_vinculo_id | BIGINT | FK tipo_vinculo |
| data_inicio | DATE | NOT NULL |
| data_fim | DATE | opcional |
| carga_semanal_min | INTEGER | NOT NULL, >= 0 |
| ativo | BOOLEAN | default TRUE |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

## projeto

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| laboratorio_id | BIGINT | FK laboratorio |
| titulo | VARCHAR(200) | NOT NULL |
| descricao | TEXT | opcional |
| data_inicio | DATE | opcional |
| data_fim | DATE | opcional |
| situacao | VARCHAR(30) | PLANEJADO, ATIVO, CONCLUIDO ou CANCELADO |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

## participante_projeto

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| participante_id | BIGINT | FK participante |
| projeto_id | BIGINT | FK projeto |
| data_inicio | DATE | NOT NULL |
| data_fim | DATE | opcional |

## cartao_rfid

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| uid | VARCHAR(64) | UNIQUE, NOT NULL |
| ativo | BOOLEAN | default TRUE |
| data_emissao | DATE | opcional |
| data_bloqueio | DATE | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |

## cartao_participante

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| cartao_rfid_id | BIGINT | FK cartao_rfid |
| participante_id | BIGINT | FK participante |
| data_inicio | TIMESTAMPTZ | NOT NULL |
| data_fim | TIMESTAMPTZ | opcional |
| ativo | BOOLEAN | default TRUE |

A aplicação deverá garantir apenas uma atribuição ativa por cartão.

## terminal

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| laboratorio_id | BIGINT | FK laboratorio |
| codigo | VARCHAR(80) | UNIQUE |
| nome | VARCHAR(120) | NOT NULL |
| descricao | TEXT | opcional |
| chave_api_hash | VARCHAR(255) | NOT NULL |
| ativo | BOOLEAN | default TRUE |
| ultimo_contato | TIMESTAMPTZ | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

## programacao

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| data_inicio | DATE | NOT NULL |
| data_fim | DATE | opcional |
| carga_semanal_prevista_min | INTEGER | >= 0 |
| ativo | BOOLEAN | default TRUE |
| created_at | TIMESTAMPTZ | NOT NULL |

## programacao_dia

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| programacao_id | BIGINT | FK programacao |
| dia_semana | SMALLINT | 1 a 7 |
| hora_entrada | TIME | opcional |
| hora_saida | TIME | opcional |
| intervalo_previsto_min | INTEGER | default 0 |
| carga_prevista_min | INTEGER | >= 0 |

Restrição única: `programacao_id + dia_semana`.

## evento_rfid

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| event_uuid | VARCHAR(120) | UNIQUE, idempotência |
| terminal_id | BIGINT | FK terminal |
| cartao_rfid_id | BIGINT | FK opcional |
| uid_recebido | VARCHAR(64) | NOT NULL |
| timestamp_dispositivo | TIMESTAMPTZ | NOT NULL |
| timestamp_servidor | TIMESTAMPTZ | NOT NULL |
| status | VARCHAR(30) | RECEBIDO, PROCESSADO, NAO_RECONHECIDO ou ERRO |
| payload_raw | JSONB | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |

## registro_ponto

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| evento_rfid_id | BIGINT | FK opcional |
| data_hora | TIMESTAMPTZ | NOT NULL |
| tipo | VARCHAR(30) | ENTRADA, SAIDA_INTERVALO, RETORNO_INTERVALO ou SAIDA |
| origem | VARCHAR(30) | RFID, AJUSTE_APROVADO ou ADMINISTRATIVO |
| status | VARCHAR(30) | ATIVO, INVALIDADO ou SUBSTITUIDO |
| created_at | TIMESTAMPTZ | NOT NULL |

## ocorrencia_ponto

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| data_referencia | DATE | NOT NULL |
| tipo | VARCHAR(50) | classificação da inconsistência |
| descricao | TEXT | NOT NULL |
| status | VARCHAR(30) | ABERTA, RESOLVIDA ou IGNORADA |
| created_at | TIMESTAMPTZ | NOT NULL |
| resolved_at | TIMESTAMPTZ | opcional |

## jornada_diaria

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| data | DATE | NOT NULL |
| carga_prevista_min | INTEGER | >= 0 |
| carga_realizada_min | INTEGER | >= 0 |
| saldo_min | INTEGER | pode ser negativo |
| situacao | VARCHAR(40) | status consolidado |
| updated_at | TIMESTAMPTZ | NOT NULL |

Restrição única: `vinculo_id + data`.

## atividade_diaria

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| jornada_diaria_id | BIGINT | FK jornada_diaria |
| projeto_id | BIGINT | FK projeto, opcional |
| descricao | TEXT | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

Não existe campo de horas editável.

## evento_calendario

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| laboratorio_id | BIGINT | FK laboratorio |
| tipo | VARCHAR(30) | FERIADO, RECESSO ou SUSPENSAO |
| descricao | VARCHAR(255) | NOT NULL |
| data_inicio | DATE | NOT NULL |
| data_fim | DATE | NOT NULL |

## afastamento

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| tipo | VARCHAR(80) | NOT NULL |
| data_inicio | DATE | NOT NULL |
| data_fim | DATE | NOT NULL |
| descricao | TEXT | opcional |
| status | VARCHAR(30) | ATIVO, ENCERRADO ou CANCELADO |
| created_at | TIMESTAMPTZ | NOT NULL |

## justificativa

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| data_referencia | DATE | NOT NULL |
| tipo | VARCHAR(50) | NOT NULL |
| descricao | TEXT | NOT NULL |
| status | VARCHAR(30) | PENDENTE, APROVADA ou REJEITADA |
| analisado_por | BIGINT | FK usuario, opcional |
| data_analise | TIMESTAMPTZ | opcional |
| observacao_coordenador | TEXT | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |

## solicitacao_ajuste

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| registro_ponto_id | BIGINT | FK opcional |
| data_referencia | DATE | NOT NULL |
| tipo_solicitado | VARCHAR(30) | tipo de ponto desejado |
| horario_solicitado | TIMESTAMPTZ | NOT NULL |
| justificativa | TEXT | NOT NULL |
| status | VARCHAR(30) | PENDENTE, APROVADA ou REJEITADA |
| analisado_por | BIGINT | FK usuario, opcional |
| data_analise | TIMESTAMPTZ | opcional |
| observacao_coordenador | TEXT | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |

## relatorio_semanal

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| vinculo_id | BIGINT | FK vinculo |
| data_inicio | DATE | NOT NULL |
| data_fim | DATE | NOT NULL |
| carga_prevista_min | INTEGER | >= 0 |
| carga_realizada_min | INTEGER | >= 0 |
| saldo_min | INTEGER | pode ser negativo |
| resumo | TEXT | opcional |
| status | VARCHAR(30) | EM_PREENCHIMENTO, ENVIADO, APROVADO ou DEVOLVIDO |
| data_envio | TIMESTAMPTZ | opcional |
| data_aprovacao | TIMESTAMPTZ | opcional |
| aprovado_por | BIGINT | FK usuario, opcional |
| observacao_coordenador | TEXT | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |
| updated_at | TIMESTAMPTZ | NOT NULL |

Restrição única: `vinculo_id + data_inicio + data_fim`.

## auditoria

| Campo | Tipo | Regra |
| --- | --- | --- |
| id | BIGSERIAL | PK |
| usuario_id | BIGINT | FK usuario, opcional |
| acao | VARCHAR(100) | NOT NULL |
| entidade | VARCHAR(100) | NOT NULL |
| entidade_id | BIGINT | opcional |
| dados_anteriores | JSONB | opcional |
| dados_novos | JSONB | opcional |
| ip | VARCHAR(64) | opcional |
| created_at | TIMESTAMPTZ | NOT NULL |
""")

write_file("database/diagrams/erd.md", """
# ERD — CheckPonto

O diagrama abaixo utiliza Mermaid e pode ser renderizado pelo GitHub.

```mermaid
erDiagram
    USUARIO ||--o| PARTICIPANTE : possui
    USUARIO ||--o{ USUARIO_LABORATORIO : autorizado
    LABORATORIO ||--o{ USUARIO_LABORATORIO : possui

    PARTICIPANTE ||--o{ VINCULO : possui
    LABORATORIO ||--o{ VINCULO : recebe
    TIPO_VINCULO ||--o{ VINCULO : classifica

    LABORATORIO ||--o{ PROJETO : possui
    PARTICIPANTE ||--o{ PARTICIPANTE_PROJETO : participa
    PROJETO ||--o{ PARTICIPANTE_PROJETO : inclui

    CARTAO_RFID ||--o{ CARTAO_PARTICIPANTE : atribuicao
    PARTICIPANTE ||--o{ CARTAO_PARTICIPANTE : utiliza

    LABORATORIO ||--o{ TERMINAL : possui
    TERMINAL ||--o{ EVENTO_RFID : produz
    CARTAO_RFID o|--o{ EVENTO_RFID : reconhecido_como

    VINCULO ||--o{ PROGRAMACAO : possui
    PROGRAMACAO ||--o{ PROGRAMACAO_DIA : detalha

    VINCULO ||--o{ REGISTRO_PONTO : possui
    EVENTO_RFID o|--o| REGISTRO_PONTO : interpretado_como

    VINCULO ||--o{ OCORRENCIA_PONTO : gera
    VINCULO ||--o{ JORNADA_DIARIA : consolida
    JORNADA_DIARIA ||--o{ ATIVIDADE_DIARIA : descreve
    PROJETO o|--o{ ATIVIDADE_DIARIA : referencia

    LABORATORIO ||--o{ EVENTO_CALENDARIO : possui

    VINCULO ||--o{ AFASTAMENTO : possui
    VINCULO ||--o{ JUSTIFICATIVA : apresenta
    VINCULO ||--o{ SOLICITACAO_AJUSTE : solicita
    REGISTRO_PONTO o|--o{ SOLICITACAO_AJUSTE : referencia

    VINCULO ||--o{ RELATORIO_SEMANAL : gera

    USUARIO o|--o{ JUSTIFICATIVA : analisa
    USUARIO o|--o{ SOLICITACAO_AJUSTE : analisa
    USUARIO o|--o{ RELATORIO_SEMANAL : aprova
    USUARIO o|--o{ AUDITORIA : executa
```

## Observação

Este ERD representa o modelo lógico inicial. A migration SQL será criada na
etapa seguinte, após a validação deste modelo.
""")

write_file("database/schema_initial.sql", """
-- ============================================================
-- CHECKPONTO
-- Modelo PostgreSQL inicial para revisão.
-- Ainda não é a migration oficial.
-- ============================================================

CREATE TABLE usuario (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil VARCHAR(30) NOT NULL
        CHECK (perfil IN ('COORDENADOR', 'PARTICIPANTE')),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE laboratorio (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    sigla VARCHAR(30) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE usuario_laboratorio (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuario(id) ON DELETE RESTRICT,
    laboratorio_id BIGINT NOT NULL REFERENCES laboratorio(id) ON DELETE RESTRICT,
    papel VARCHAR(30) NOT NULL CHECK (papel IN ('COORDENADOR')),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (usuario_id, laboratorio_id, papel)
);

CREATE TABLE participante (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL UNIQUE REFERENCES usuario(id) ON DELETE RESTRICT,
    matricula VARCHAR(80),
    situacao VARCHAR(30) NOT NULL DEFAULT 'ATIVO'
        CHECK (situacao IN ('ATIVO','INATIVO','CONCLUIDO','AFASTADO')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE tipo_vinculo (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL UNIQUE,
    carga_semanal_padrao_min INTEGER NOT NULL DEFAULT 0
        CHECK (carga_semanal_padrao_min >= 0),
    carga_diaria_minima_min INTEGER
        CHECK (carga_diaria_minima_min IS NULL OR carga_diaria_minima_min >= 0),
    carga_diaria_maxima_min INTEGER
        CHECK (carga_diaria_maxima_min IS NULL OR carga_diaria_maxima_min >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CHECK (
        carga_diaria_minima_min IS NULL
        OR carga_diaria_maxima_min IS NULL
        OR carga_diaria_maxima_min >= carga_diaria_minima_min
    )
);

CREATE TABLE vinculo (
    id BIGSERIAL PRIMARY KEY,
    participante_id BIGINT NOT NULL REFERENCES participante(id) ON DELETE RESTRICT,
    laboratorio_id BIGINT NOT NULL REFERENCES laboratorio(id) ON DELETE RESTRICT,
    tipo_vinculo_id BIGINT NOT NULL REFERENCES tipo_vinculo(id) ON DELETE RESTRICT,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    carga_semanal_min INTEGER NOT NULL CHECK (carga_semanal_min >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE projeto (
    id BIGSERIAL PRIMARY KEY,
    laboratorio_id BIGINT NOT NULL REFERENCES laboratorio(id) ON DELETE RESTRICT,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    data_inicio DATE,
    data_fim DATE,
    situacao VARCHAR(30) NOT NULL DEFAULT 'ATIVO'
        CHECK (situacao IN ('PLANEJADO','ATIVO','CONCLUIDO','CANCELADO')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (data_fim IS NULL OR data_inicio IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE participante_projeto (
    id BIGSERIAL PRIMARY KEY,
    participante_id BIGINT NOT NULL REFERENCES participante(id) ON DELETE RESTRICT,
    projeto_id BIGINT NOT NULL REFERENCES projeto(id) ON DELETE RESTRICT,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    CHECK (data_fim IS NULL OR data_fim >= data_inicio),
    UNIQUE (participante_id, projeto_id, data_inicio)
);

CREATE TABLE cartao_rfid (
    id BIGSERIAL PRIMARY KEY,
    uid VARCHAR(64) NOT NULL UNIQUE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_emissao DATE,
    data_bloqueio DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE cartao_participante (
    id BIGSERIAL PRIMARY KEY,
    cartao_rfid_id BIGINT NOT NULL REFERENCES cartao_rfid(id) ON DELETE RESTRICT,
    participante_id BIGINT NOT NULL REFERENCES participante(id) ON DELETE RESTRICT,
    data_inicio TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    data_fim TIMESTAMPTZ,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE UNIQUE INDEX uq_cartao_atribuicao_ativa
ON cartao_participante(cartao_rfid_id)
WHERE ativo = TRUE AND data_fim IS NULL;

CREATE TABLE terminal (
    id BIGSERIAL PRIMARY KEY,
    laboratorio_id BIGINT NOT NULL REFERENCES laboratorio(id) ON DELETE RESTRICT,
    codigo VARCHAR(80) NOT NULL UNIQUE,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT,
    chave_api_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    ultimo_contato TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE programacao (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    carga_semanal_prevista_min INTEGER NOT NULL
        CHECK (carga_semanal_prevista_min >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE programacao_dia (
    id BIGSERIAL PRIMARY KEY,
    programacao_id BIGINT NOT NULL REFERENCES programacao(id) ON DELETE RESTRICT,
    dia_semana SMALLINT NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
    hora_entrada TIME,
    hora_saida TIME,
    intervalo_previsto_min INTEGER NOT NULL DEFAULT 0
        CHECK (intervalo_previsto_min >= 0),
    carga_prevista_min INTEGER NOT NULL CHECK (carga_prevista_min >= 0),
    UNIQUE (programacao_id, dia_semana)
);

CREATE TABLE evento_rfid (
    id BIGSERIAL PRIMARY KEY,
    event_uuid VARCHAR(120) NOT NULL UNIQUE,
    terminal_id BIGINT NOT NULL REFERENCES terminal(id) ON DELETE RESTRICT,
    cartao_rfid_id BIGINT REFERENCES cartao_rfid(id) ON DELETE RESTRICT,
    uid_recebido VARCHAR(64) NOT NULL,
    timestamp_dispositivo TIMESTAMPTZ NOT NULL,
    timestamp_servidor TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(30) NOT NULL DEFAULT 'RECEBIDO'
        CHECK (status IN ('RECEBIDO','PROCESSADO','NAO_RECONHECIDO','ERRO')),
    payload_raw JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE registro_ponto (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    evento_rfid_id BIGINT REFERENCES evento_rfid(id) ON DELETE RESTRICT,
    data_hora TIMESTAMPTZ NOT NULL,
    tipo VARCHAR(30) NOT NULL
        CHECK (tipo IN ('ENTRADA','SAIDA_INTERVALO','RETORNO_INTERVALO','SAIDA')),
    origem VARCHAR(30) NOT NULL
        CHECK (origem IN ('RFID','AJUSTE_APROVADO','ADMINISTRATIVO')),
    status VARCHAR(30) NOT NULL DEFAULT 'ATIVO'
        CHECK (status IN ('ATIVO','INVALIDADO','SUBSTITUIDO')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX uq_registro_evento_rfid
ON registro_ponto(evento_rfid_id)
WHERE evento_rfid_id IS NOT NULL;

CREATE TABLE ocorrencia_ponto (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    data_referencia DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ABERTA'
        CHECK (status IN ('ABERTA','RESOLVIDA','IGNORADA')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

CREATE TABLE jornada_diaria (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    data DATE NOT NULL,
    carga_prevista_min INTEGER NOT NULL DEFAULT 0 CHECK (carga_prevista_min >= 0),
    carga_realizada_min INTEGER NOT NULL DEFAULT 0 CHECK (carga_realizada_min >= 0),
    saldo_min INTEGER NOT NULL DEFAULT 0,
    situacao VARCHAR(40) NOT NULL DEFAULT 'PENDENTE',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (vinculo_id, data)
);

CREATE TABLE atividade_diaria (
    id BIGSERIAL PRIMARY KEY,
    jornada_diaria_id BIGINT NOT NULL REFERENCES jornada_diaria(id) ON DELETE RESTRICT,
    projeto_id BIGINT REFERENCES projeto(id) ON DELETE RESTRICT,
    descricao TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE evento_calendario (
    id BIGSERIAL PRIMARY KEY,
    laboratorio_id BIGINT NOT NULL REFERENCES laboratorio(id) ON DELETE RESTRICT,
    tipo VARCHAR(30) NOT NULL
        CHECK (tipo IN ('FERIADO','RECESSO','SUSPENSAO')),
    descricao VARCHAR(255) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    CHECK (data_fim >= data_inicio)
);

CREATE TABLE afastamento (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    tipo VARCHAR(80) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    descricao TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'ATIVO'
        CHECK (status IN ('ATIVO','ENCERRADO','CANCELADO')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (data_fim >= data_inicio)
);

CREATE TABLE justificativa (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    data_referencia DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE'
        CHECK (status IN ('PENDENTE','APROVADA','REJEITADA')),
    analisado_por BIGINT REFERENCES usuario(id) ON DELETE RESTRICT,
    data_analise TIMESTAMPTZ,
    observacao_coordenador TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE solicitacao_ajuste (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    registro_ponto_id BIGINT REFERENCES registro_ponto(id) ON DELETE RESTRICT,
    data_referencia DATE NOT NULL,
    tipo_solicitado VARCHAR(30) NOT NULL
        CHECK (tipo_solicitado IN ('ENTRADA','SAIDA_INTERVALO','RETORNO_INTERVALO','SAIDA')),
    horario_solicitado TIMESTAMPTZ NOT NULL,
    justificativa TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE'
        CHECK (status IN ('PENDENTE','APROVADA','REJEITADA')),
    analisado_por BIGINT REFERENCES usuario(id) ON DELETE RESTRICT,
    data_analise TIMESTAMPTZ,
    observacao_coordenador TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE relatorio_semanal (
    id BIGSERIAL PRIMARY KEY,
    vinculo_id BIGINT NOT NULL REFERENCES vinculo(id) ON DELETE RESTRICT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    carga_prevista_min INTEGER NOT NULL DEFAULT 0 CHECK (carga_prevista_min >= 0),
    carga_realizada_min INTEGER NOT NULL DEFAULT 0 CHECK (carga_realizada_min >= 0),
    saldo_min INTEGER NOT NULL DEFAULT 0,
    resumo TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'EM_PREENCHIMENTO'
        CHECK (status IN ('EM_PREENCHIMENTO','ENVIADO','APROVADO','DEVOLVIDO')),
    data_envio TIMESTAMPTZ,
    data_aprovacao TIMESTAMPTZ,
    aprovado_por BIGINT REFERENCES usuario(id) ON DELETE RESTRICT,
    observacao_coordenador TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (data_fim >= data_inicio),
    UNIQUE (vinculo_id, data_inicio, data_fim)
);

CREATE TABLE auditoria (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT REFERENCES usuario(id) ON DELETE RESTRICT,
    acao VARCHAR(100) NOT NULL,
    entidade VARCHAR(100) NOT NULL,
    entidade_id BIGINT,
    dados_anteriores JSONB,
    dados_novos JSONB,
    ip VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices de consulta operacional
CREATE INDEX idx_vinculo_participante ON vinculo(participante_id);
CREATE INDEX idx_vinculo_laboratorio ON vinculo(laboratorio_id);
CREATE INDEX idx_evento_rfid_terminal_data
    ON evento_rfid(terminal_id, timestamp_dispositivo);
CREATE INDEX idx_evento_rfid_uid_data
    ON evento_rfid(uid_recebido, timestamp_dispositivo);
CREATE INDEX idx_registro_ponto_vinculo_data
    ON registro_ponto(vinculo_id, data_hora);
CREATE INDEX idx_ocorrencia_status
    ON ocorrencia_ponto(status, data_referencia);
CREATE INDEX idx_jornada_data
    ON jornada_diaria(data);
CREATE INDEX idx_justificativa_status
    ON justificativa(status, data_referencia);
CREATE INDEX idx_ajuste_status
    ON solicitacao_ajuste(status, data_referencia);
CREATE INDEX idx_relatorio_status
    ON relatorio_semanal(status, data_inicio);
CREATE INDEX idx_auditoria_entidade
    ON auditoria(entidade, entidade_id, created_at);
""")

write_file("database/README.md", """
# Banco de Dados — CheckPonto

## Tecnologia

PostgreSQL.

## Organização

- `schema_initial.sql`: modelo SQL inicial para revisão;
- `migrations/`: migrations oficiais do projeto;
- `seeds/`: dados iniciais controlados;
- `diagrams/`: diagramas do banco;
- `scripts/`: utilitários relacionados ao banco.

## Situação atual

O arquivo `schema_initial.sql` ainda não representa uma migration oficial.

A sequência planejada é:

1. definir requisitos;
2. definir modelo de domínio;
3. definir modelo lógico;
4. revisar ERD e dicionário;
5. validar SQL inicial;
6. criar a migration `001_initial_schema.sql`;
7. criar seeds;
8. executar PostgreSQL via Docker;
9. testar integridade e constraints;
10. integrar o backend.

## Regras importantes

- eventos RFID são preservados;
- `event_uuid` é único;
- horas são armazenadas em minutos;
- eventos temporais usam `TIMESTAMPTZ`;
- dados históricos não usam exclusão em cascata;
- segredos de terminais são armazenados somente como hash;
- alterações relevantes serão auditadas.
""")

print()
print("=" * 74)
print(" VALIDACAO DO MODELO")
print("=" * 74)

files = [
    "docs/04-banco-dados/modelo-logico.md",
    "docs/04-banco-dados/dicionario-dados.md",
    "database/diagrams/erd.md",
    "database/schema_initial.sql",
    "database/README.md",
]

errors = 0
for rel in files:
    p = ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        print(f"[ERRO] {rel}")
        errors += 1
    else:
        print(f"[OK] {rel} ({p.stat().st_size} bytes)")

sql = (ROOT / "database/schema_initial.sql").read_text(encoding="utf-8")
tables = [
    "usuario", "laboratorio", "usuario_laboratorio", "participante",
    "tipo_vinculo", "vinculo", "projeto", "participante_projeto",
    "cartao_rfid", "cartao_participante", "terminal", "programacao",
    "programacao_dia", "evento_rfid", "registro_ponto",
    "ocorrencia_ponto", "jornada_diaria", "atividade_diaria",
    "evento_calendario", "afastamento", "justificativa",
    "solicitacao_ajuste", "relatorio_semanal", "auditoria"
]

print()
print(f"Tabelas esperadas: {len(tables)}")

for table_name in tables:
    marker = f"CREATE TABLE {table_name} "
    if marker not in sql:
        print(f"[ERRO] Tabela não localizada no SQL: {table_name}")
        errors += 1

if "event_uuid VARCHAR(120) NOT NULL UNIQUE" in sql:
    print("[OK] Idempotência RFID definida por event_uuid UNIQUE.")
else:
    print("[ERRO] Restrição de idempotência não localizada.")
    errors += 1

if "payload_raw JSONB" in sql:
    print("[OK] Payload bruto RFID preservável em JSONB.")
else:
    print("[ERRO] payload_raw JSONB não localizado.")
    errors += 1

if "dados_anteriores JSONB" in sql and "dados_novos JSONB" in sql:
    print("[OK] Auditoria estruturada em JSONB.")
else:
    print("[ERRO] Campos JSONB de auditoria não localizados.")
    errors += 1

if "ON DELETE CASCADE" not in sql:
    print("[OK] Nenhuma exclusão em cascata foi introduzida no histórico.")
else:
    print("[ERRO] ON DELETE CASCADE encontrado.")
    errors += 1

print()
if errors:
    print("=" * 74)
    print(f" MODELO GERADO COM {errors} PROBLEMA(S)")
    print("=" * 74)
    sys.exit(1)

print("=" * 74)
print(" MODELO LOGICO CONFIGURADO COM SUCESSO")
print("=" * 74)
print(f"Tabelas previstas: {len(tables)}")
print("Artefato SQL: database/schema_initial.sql")
print("Proxima etapa: revisar e converter em migration PostgreSQL oficial.")
