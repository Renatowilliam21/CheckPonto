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
