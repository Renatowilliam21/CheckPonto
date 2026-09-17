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
