# Regras de Negócio

| ID | Regra |
| --- | --- |
| **RN01** | Todo participante deverá possuir vínculo ativo com um laboratório para registrar ponto. |
| **RN02** | Cada cartão RFID ativo deverá estar associado a um único participante. |
| **RN03** | O participante poderá possuir tipos de vínculo, inicialmente Bolsista ou Estagiário. |
| **RN04** | Bolsistas terão como regra inicial carga obrigatória de 16 horas semanais. |
| **RN05** | A programação semanal do bolsista será definida pelo coordenador, considerando normalmente jornadas entre 4 e 6 horas por dia. |
| **RN06** | Estagiários poderão possuir programação variável, incluindo jornadas previstas de 4 ou 8 horas. |
| **RN07** | As regras de carga horária serão configuradas no servidor conforme o vínculo e não fixadas no firmware. |
| **RN08** | O registro oficial de presença será originado prioritariamente pelo RFID. |
| **RN09** | O participante não selecionará manualmente se a batida representa entrada ou saída. |
| **RN10** | Uma jornada sem intervalo poderá ser composta por entrada e saída. |
| **RN11** | Uma jornada com almoço deverá considerar saída e retorno do intervalo. |
| **RN12** | O intervalo de almoço não será contabilizado como tempo trabalhado. |
| **RN13** | Batidas incompletas ou inconsistentes deverão gerar ocorrência. |
| **RN14** | O participante não poderá alterar diretamente um registro originado pelo RFID. |
| **RN15** | Correções de ponto deverão ser solicitadas pelo participante e analisadas pelo coordenador. |
| **RN16** | Toda correção deverá preservar o registro original e seu histórico. |
| **RN17** | A carga realizada será calculada a partir dos registros válidos e das correções aprovadas. |
| **RN18** | Cada participante deverá possuir programação semanal individual. |
| **RN19** | Feriados e recessos não deverão gerar automaticamente falta ou carga pendente. |
| **RN20** | Afastamentos individuais não deverão produzir faltas durante sua vigência. |
| **RN21** | Ausências poderão ser classificadas como justificadas ou não justificadas. |
| **RN22** | As justificativas deverão ser analisadas pelo coordenador. |
| **RN23** | O participante deverá registrar a descrição das atividades desenvolvidas diariamente. |
| **RN24** | A carga horária apresentada junto à atividade será obtida automaticamente do controle de ponto. |
| **RN25** | O participante deverá registrar um resumo semanal das atividades. |
| **RN26** | O sistema deverá consolidar automaticamente carga prevista e realizada no fechamento semanal. |
| **RN27** | O relatório semanal poderá assumir os estados EM_PREENCHIMENTO, ENVIADO, APROVADO e DEVOLVIDO. |
| **RN28** | Um relatório devolvido poderá ser corrigido e reenviado. |
| **RN29** | Alterações posteriores à aprovação deverão ser controladas e registradas. |
| **RN30** | O sistema deverá manter histórico de registros, correções, justificativas e aprovações. |
