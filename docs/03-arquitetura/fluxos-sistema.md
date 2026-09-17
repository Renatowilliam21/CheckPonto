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
           /            coordenador   coordenador
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
