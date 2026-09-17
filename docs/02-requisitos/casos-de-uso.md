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
