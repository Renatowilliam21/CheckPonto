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
