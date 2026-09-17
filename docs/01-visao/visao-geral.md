# CheckPonto — Visão Geral

## 1. Apresentação

O CheckPonto é uma plataforma para acompanhamento de bolsistas e estagiários vinculados a laboratórios.

O sistema integra controle de frequência por RFID, acompanhamento da carga horária, registro das atividades desenvolvidas e geração de relatórios.

A solução será composta por aplicação web, API REST, banco de dados, terminal RFID baseado em ESP32 e infraestrutura de implantação.

## 2. Problema

O acompanhamento manual da frequência dificulta a verificação da carga horária efetivamente cumprida e a associação entre o período de permanência no laboratório e as atividades desenvolvidas.

O sistema busca reduzir problemas relacionados a esquecimento de registros, divergências de horários, controle da carga semanal, justificativas, acompanhamento das atividades, consolidação de relatórios e rastreabilidade das correções.

## 3. Objetivo geral

Desenvolver uma plataforma integrada para registrar, acompanhar e consolidar a frequência, a carga horária e as atividades desenvolvidas por bolsistas e estagiários de laboratório.

## 4. Objetivos específicos

- registrar presença utilizando RFID;
- calcular automaticamente a carga horária realizada;
- permitir programação semanal individual;
- acompanhar o cumprimento da carga horária;
- registrar atividades desenvolvidas diariamente;
- consolidar atividades em relatórios semanais;
- controlar faltas e justificativas;
- considerar feriados, recessos e afastamentos;
- permitir correções controladas de ponto;
- fornecer dashboards;
- gerar relatórios por participante e período;
- preservar o histórico das operações relevantes.

## 5. Arquitetura geral

```text
Cartão RFID -> RC522 -> ESP32 -> API REST -> PostgreSQL
                                      |
                                      +-> Aplicação Web
```

## 6. Usuários

Inicialmente o sistema atenderá coordenadores, bolsistas e estagiários. A arquitetura deverá permitir expansão futura para outros laboratórios e tipos de vínculo.
