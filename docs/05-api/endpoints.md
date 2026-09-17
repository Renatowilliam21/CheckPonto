# Endpoints Planejados — CheckPonto

> Este documento é uma especificação inicial para orientar o desenvolvimento.
> Os endpoints poderão ser refinados durante a implementação, desde que as
> mudanças sejam documentadas.

Base sugerida: `/api/v1`.

## 1. Autenticação

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| POST | `/auth/login` | Autenticar usuário |
| GET | `/auth/me` | Consultar usuário autenticado |

## 2. Participantes

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/participantes` | Listar participantes |
| POST | `/participantes` | Cadastrar participante |
| GET | `/participantes/:id` | Consultar participante |
| PATCH | `/participantes/:id` | Atualizar participante |
| PATCH | `/participantes/:id/status` | Alterar situação |

## 3. Laboratórios

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/laboratorios` | Listar laboratórios |
| POST | `/laboratorios` | Cadastrar laboratório |
| GET | `/laboratorios/:id` | Consultar laboratório |
| PATCH | `/laboratorios/:id` | Atualizar laboratório |

## 4. Vínculos

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/vinculos` | Listar vínculos |
| POST | `/vinculos` | Criar vínculo |
| GET | `/vinculos/:id` | Consultar vínculo |
| PATCH | `/vinculos/:id` | Atualizar vínculo |
| PATCH | `/vinculos/:id/encerrar` | Encerrar vínculo |

## 5. Projetos

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/projetos` | Listar projetos |
| POST | `/projetos` | Cadastrar projeto |
| GET | `/projetos/:id` | Consultar projeto |
| PATCH | `/projetos/:id` | Atualizar projeto |
| POST | `/projetos/:id/participantes` | Associar participante |

## 6. Cartões RFID

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/cartoes` | Listar cartões |
| POST | `/cartoes` | Cadastrar cartão |
| POST | `/cartoes/:id/atribuir` | Atribuir cartão |
| PATCH | `/cartoes/:id/bloquear` | Bloquear cartão |

## 7. Terminais

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/terminais` | Listar terminais |
| POST | `/terminais` | Cadastrar terminal |
| GET | `/terminais/:id` | Consultar terminal |
| PATCH | `/terminais/:id` | Atualizar terminal |

## 8. Ingestão RFID

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| POST | `/rfid/eventos` | Receber evento do ESP32 |

Exemplo:

```json
{
  "event_id": "PONTO01-20260917-00001284",
  "device_id": "PONTO01",
  "card_uid": "A37F219C",
  "timestamp": "2026-09-17T08:01:03-03:00"
}
```

A API deverá tratar `event_id` de forma idempotente.

## 9. Programação semanal

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/vinculos/:id/programacoes` | Histórico |
| POST | `/vinculos/:id/programacoes` | Criar programação |
| GET | `/programacoes/:id` | Consultar programação |

## 10. Ponto e jornadas

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/pontos` | Consultar registros |
| GET | `/jornadas` | Consultar jornadas |
| GET | `/jornadas/:id` | Detalhar jornada |
| GET | `/ocorrencias-ponto` | Consultar inconsistências |

## 11. Atividades

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/atividades` | Consultar atividades |
| POST | `/atividades` | Registrar atividade |
| PATCH | `/atividades/:id` | Editar descrição |

A carga horária não deve ser recebida como campo editável da atividade.

## 12. Justificativas e ajustes

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| POST | `/justificativas` | Enviar justificativa |
| GET | `/justificativas` | Consultar justificativas |
| PATCH | `/justificativas/:id/analisar` | Aprovar/rejeitar |
| POST | `/ajustes-ponto` | Solicitar correção |
| GET | `/ajustes-ponto` | Consultar solicitações |
| PATCH | `/ajustes-ponto/:id/analisar` | Aprovar/rejeitar |

## 13. Calendário e afastamentos

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/calendario` | Consultar eventos |
| POST | `/calendario` | Cadastrar evento |
| POST | `/afastamentos` | Cadastrar afastamento |
| GET | `/afastamentos` | Consultar afastamentos |

## 14. Relatórios semanais

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/relatorios-semanais` | Listar |
| GET | `/relatorios-semanais/:id` | Detalhar |
| POST | `/relatorios-semanais/:id/enviar` | Enviar |
| POST | `/relatorios-semanais/:id/aprovar` | Aprovar |
| POST | `/relatorios-semanais/:id/devolver` | Devolver |

## 15. Dashboards

| Método | Endpoint | Objetivo |
| --- | --- | --- |
| GET | `/dashboard/participante` | Dados do participante |
| GET | `/dashboard/coordenador` | Dados administrativos |
| GET | `/dashboard/presentes` | Participantes presentes |

## 16. Convenções

- JSON como formato principal;
- datas e horários em ISO 8601;
- autenticação obrigatória quando aplicável;
- respostas HTTP coerentes;
- validação no backend;
- paginação em listagens extensas;
- mensagens de erro sem exposição de dados sensíveis.
