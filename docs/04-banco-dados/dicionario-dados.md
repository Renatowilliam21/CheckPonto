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
