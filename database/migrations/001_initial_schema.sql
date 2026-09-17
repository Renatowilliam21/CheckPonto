-- ============================================================
-- CHECKPONTO
-- Migration 001 - Esquema inicial
--
-- Regra:
-- Este arquivo representa a primeira versao oficial do schema.
-- Depois de aplicado em ambientes compartilhados, nao deve ser
-- reescrito; alteracoes futuras devem usar novas migrations.
-- ============================================================

BEGIN;

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

COMMIT;
