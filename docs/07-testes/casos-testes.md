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
