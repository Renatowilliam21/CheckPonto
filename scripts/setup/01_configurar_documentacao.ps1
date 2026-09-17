$ErrorActionPreference = "Stop"

# ============================================================
# CHECKPONTO
# Script 01 - Configuracao da documentacao inicial
# Executar a partir da raiz do projeto CheckPonto
# ============================================================

$Root = (Get-Location).Path

Write-Host ""
Write-Host "============================================================"
Write-Host " CHECKPONTO - DOCUMENTACAO INICIAL"
Write-Host "============================================================"
Write-Host ""

# ------------------------------------------------------------
# 1. Validacao da raiz
# ------------------------------------------------------------

$RequiredDirs = @(
    "docs\01-visao",
    "docs\02-requisitos",
    "docs\03-arquitetura",
    "docs\04-banco-dados"
)

foreach ($Dir in $RequiredDirs) {
    $Path = Join-Path $Root $Dir

    if (-not (Test-Path $Path)) {
        throw "[ERRO] Estrutura do CheckPonto nao encontrada: $Dir"
    }
}

Write-Host "[OK] Estrutura do projeto localizada."
Write-Host "[OK] Raiz: $Root"

# ------------------------------------------------------------
# Funcao auxiliar
# ------------------------------------------------------------

function Write-ProjectFile {
    param (
        [string]$RelativePath,
        [string]$Content
    )

    $Path = Join-Path $Root $RelativePath
    Set-Content -Path $Path -Value $Content -Encoding UTF8

    if (-not (Test-Path $Path)) {
        throw "[ERRO] Falha ao criar $RelativePath"
    }

    Write-Host "[OK] $RelativePath"
}

# ============================================================
# 2. VISAO GERAL
# ============================================================

$Content = @'
# Visao Geral do CheckPonto

## 1. Apresentacao

O CheckPonto e um sistema para acompanhamento de bolsistas e
estagiarios vinculados a laboratorios.

A plataforma integra registro de frequencia por RFID, controle de
carga horaria, acompanhamento das atividades desenvolvidas e
geracao de relatorios.

O sistema possui como principal usuario administrativo o coordenador
do laboratorio e oferece acesso individual aos participantes.

## 2. Problema

O acompanhamento manual da frequencia de bolsistas e estagiarios
dificulta a verificacao da carga horaria efetivamente cumprida e a
associacao entre o periodo trabalhado e as atividades desenvolvidas.

O CheckPonto busca centralizar essas informacoes em uma unica
plataforma.

## 3. Objetivo Geral

Desenvolver uma plataforma integrada para registrar, acompanhar e
consolidar a frequencia, a carga horaria e as atividades desenvolvidas
por bolsistas e estagiarios de laboratorio.

## 4. Objetivos Especificos

- registrar presenca utilizando RFID;
- calcular automaticamente a carga horaria realizada;
- permitir programacao semanal individual;
- acompanhar o cumprimento da carga horaria;
- registrar atividades desenvolvidas diariamente;
- consolidar as atividades em relatorios semanais;
- controlar faltas e justificativas;
- considerar feriados, recessos e afastamentos;
- permitir correcoes controladas de registros;
- fornecer dashboards para participantes e coordenadores;
- gerar relatorios por participante e periodo;
- manter rastreabilidade das operacoes relevantes.

## 5. Arquitetura Geral

Cartao RFID -> RC522 -> ESP32 -> API REST -> Banco de Dados
                                      |
                                      +-> Aplicacao Web

## 6. Publico-alvo

Inicialmente:

- bolsistas de laboratorio;
- estagiarios;
- coordenadores de laboratorio.

A arquitetura devera permitir expansao futura para outros laboratorios
e tipos de vinculo.
'@

Write-ProjectFile "docs\01-visao\visao-geral.md" $Content

# ============================================================
# 3. ESCOPO
# ============================================================

$Content = @'
# Escopo do CheckPonto

## 1. Escopo da primeira versao

A primeira versao do CheckPonto devera contemplar:

### Gestao

- autenticacao;
- cadastro de usuarios;
- cadastro de participantes;
- cadastro de laboratorios;
- cadastro de projetos;
- cadastro de tipos de vinculo;
- associacao entre participante e projeto;
- associacao entre participante e cartao RFID.

### Frequencia

- registro por RFID;
- entrada;
- saida;
- saida para almoco;
- retorno do almoco;
- calculo diario de horas;
- calculo semanal;
- identificacao de inconsistencias;
- funcionamento temporariamente offline do terminal;
- sincronizacao posterior.

### Planejamento

- programacao semanal individual;
- carga horaria prevista;
- comparacao entre horas previstas e realizadas.

### Ocorrencias

- faltas justificadas;
- faltas nao justificadas;
- feriados;
- recessos;
- afastamentos;
- solicitacao de correcao de ponto;
- aprovacao ou rejeicao pelo coordenador.

### Atividades

- descricao diaria das atividades;
- resumo semanal;
- consolidacao das atividades com a carga horaria;
- envio do relatorio semanal;
- aprovacao ou devolucao pelo coordenador.

### Relatorios

- relatorio semanal;
- relatorio mensal;
- relatorio por periodo;
- carga prevista;
- carga realizada;
- atividades desenvolvidas;
- ocorrencias;
- exportacao em PDF.

## 2. Fora do escopo inicial

Nao fazem parte obrigatoria da primeira versao:

- reconhecimento facial;
- biometria;
- aplicativo mobile nativo;
- folha de pagamento;
- controle financeiro de bolsas;
- geolocalizacao do participante;
- inteligencia artificial;
- WhatsApp ou Telegram;
- integracao com sistemas institucionais;
- assinatura digital certificada.

Esses recursos poderao ser avaliados como trabalhos futuros.
'@

Write-ProjectFile "docs\01-visao\escopo.md" $Content

# ============================================================
# 4. ATORES
# ============================================================

$Content = @'
# Atores do Sistema

## Coordenador

Responsavel pela administracao e acompanhamento do laboratorio.

Principais responsabilidades:

- cadastrar participantes;
- cadastrar vinculos;
- cadastrar projetos;
- associar cartoes RFID;
- configurar programacoes semanais;
- acompanhar frequencia;
- acompanhar carga horaria;
- analisar justificativas;
- analisar solicitacoes de correcao;
- acompanhar atividades;
- aprovar ou devolver relatorios;
- consultar dashboards;
- gerar relatorios.

## Participante

Representa bolsistas e estagiarios.

Principais responsabilidades:

- realizar registro fisico pelo RFID;
- acessar sua conta;
- consultar sua programacao;
- consultar horas realizadas;
- consultar saldo semanal;
- registrar atividades diarias;
- preencher resumo semanal;
- enviar relatorio semanal;
- apresentar justificativas;
- solicitar correcoes;
- acompanhar seus relatorios.

## Terminal RFID

Dispositivo baseado em ESP32 responsavel pela coleta dos eventos
fisicos.

Responsabilidades:

- ler o UID do cartao;
- identificar o evento;
- registrar data e hora;
- enviar o evento para a API;
- fornecer retorno visual ou sonoro;
- armazenar eventos quando estiver offline;
- sincronizar eventos pendentes.
'@

Write-ProjectFile "docs\01-visao\atores.md" $Content

# ============================================================
# 5. REGRAS DE NEGOCIO
# ============================================================

$Rules = @(
"RN01|Todo participante devera possuir vinculo ativo com um laboratorio para realizar registros de ponto.",
"RN02|Cada cartao RFID ativo devera estar associado a um unico participante.",
"RN03|Um participante podera possuir diferentes tipos de vinculo, inicialmente Bolsista ou Estagiario.",
"RN04|Bolsistas deverao cumprir, como regra inicial, 16 horas semanais.",
"RN05|A programacao semanal do bolsista devera ser cadastrada pelo coordenador, considerando jornadas diarias normalmente entre 4 e 6 horas.",
"RN06|Estagiarios poderao possuir programacao variavel, inclusive jornadas previstas de 4 ou 8 horas.",
"RN07|As regras de carga horaria deverao ser configuraveis por vinculo e nao fixadas no firmware.",
"RN08|O registro oficial de presenca devera ser originado prioritariamente pelo cartao RFID.",
"RN09|O participante nao precisara selecionar manualmente entrada ou saida.",
"RN10|Jornadas sem intervalo para almoco poderao possuir apenas entrada e saida.",
"RN11|Quando houver intervalo para almoco deverao existir registros correspondentes a saida e retorno.",
"RN12|O intervalo de almoco nao devera ser contabilizado como carga horaria trabalhada.",
"RN13|Batidas incompletas ou inconsistentes deverao gerar ocorrencia.",
"RN14|O participante nao podera alterar diretamente um registro RFID.",
"RN15|Correcoes deverao ser solicitadas e analisadas pelo coordenador.",
"RN16|Alteracoes deverao preservar os dados originais para auditoria.",
"RN17|A carga realizada sera calculada a partir dos registros validos e correcoes aprovadas.",
"RN18|Cada participante devera possuir programacao semanal individual.",
"RN19|Feriados e recessos nao deverao gerar automaticamente falta ou carga pendente.",
"RN20|Afastamentos nao deverao produzir faltas durante sua vigencia.",
"RN21|Ausencias poderao ser classificadas como justificadas ou nao justificadas.",
"RN22|Justificativas deverao ser analisadas pelo coordenador.",
"RN23|O participante devera registrar descricao das atividades desenvolvidas.",
"RN24|A carga horaria apresentada junto a atividade sera proveniente do controle de ponto.",
"RN25|O participante devera registrar resumo semanal das atividades.",
"RN26|O sistema devera consolidar carga prevista e realizada no fechamento semanal.",
"RN27|O relatorio semanal podera assumir os estados Em preenchimento, Enviado, Aprovado e Devolvido.",
"RN28|Relatorios devolvidos poderao ser corrigidos e reenviados.",
"RN29|Alteracoes posteriores a aprovacao deverao ser registradas no historico.",
"RN30|O sistema devera manter historico de registros, correcoes, justificativas e aprovacoes."
)

$Content = "# Regras de Negocio`r`n`r`n"
$Content += "| ID | Regra |`r`n"
$Content += "|---|---|`r`n"

foreach ($Rule in $Rules) {
    $Parts = $Rule -split "\|", 2
    $Content += "| **$($Parts[0])** | $($Parts[1]) |`r`n"
}

Write-ProjectFile "docs\02-requisitos\regras-negocio.md" $Content

# ============================================================
# 6. REQUISITOS FUNCIONAIS
# ============================================================

$RF = @(
"RF01|Permitir autenticacao por login e senha.",
"RF02|Permitir ao coordenador cadastrar, consultar, alterar e desativar participantes.",
"RF03|Permitir atribuir perfis de acesso.",
"RF04|Permitir ao participante acessar suas informacoes individuais.",
"RF05|Impedir acesso nao autorizado aos dados de outros participantes.",
"RF06|Permitir cadastrar e gerenciar laboratorios.",
"RF07|Permitir associar coordenadores aos laboratorios.",
"RF08|Permitir cadastrar projetos.",
"RF09|Permitir associar participantes aos projetos.",
"RF10|Permitir cadastrar tipos de vinculo.",
"RF11|Permitir associar vinculos aos participantes.",
"RF12|Permitir cadastrar cartoes RFID.",
"RF13|Permitir associar cartao RFID a participante.",
"RF14|Permitir ativar ou bloquear cartao RFID.",
"RF15|Permitir cadastrar terminais RFID.",
"RF16|O terminal deve identificar o UID do cartao.",
"RF17|O terminal deve transmitir eventos para a API.",
"RF18|O terminal deve fornecer confirmacao visual ou sonora.",
"RF19|O terminal deve armazenar temporariamente eventos sem comunicacao.",
"RF20|O terminal deve sincronizar eventos pendentes.",
"RF21|Permitir ao coordenador cadastrar programacao semanal individual.",
"RF22|Permitir definir dias, horarios e carga prevista.",
"RF23|Calcular carga horaria semanal prevista.",
"RF24|Permitir programacoes diferentes conforme o vinculo.",
"RF25|Preservar historico das programacoes anteriores.",
"RF26|Registrar data, hora, cartao, participante e terminal da batida.",
"RF27|Interpretar automaticamente a sequencia das batidas.",
"RF28|Identificar jornadas com e sem intervalo de almoco.",
"RF29|Calcular automaticamente carga horaria diaria.",
"RF30|Descontar o intervalo de almoco.",
"RF31|Calcular carga horaria semanal realizada.",
"RF32|Comparar carga prevista e realizada.",
"RF33|Identificar registros incompletos ou inconsistentes.",
"RF34|Permitir solicitacao de correcao de ponto.",
"RF35|Exigir justificativa na solicitacao de correcao.",
"RF36|Permitir ao coordenador aprovar ou rejeitar correcoes.",
"RF37|Manter registro original e historico das correcoes.",
"RF38|Registrar faltas justificadas e nao justificadas.",
"RF39|Permitir ao participante apresentar justificativa de ausencia.",
"RF40|Permitir ao coordenador analisar justificativas.",
"RF41|Permitir cadastrar feriados.",
"RF42|Permitir cadastrar recessos.",
"RF43|Permitir cadastrar afastamentos.",
"RF44|Considerar eventos do calendario e afastamentos no calculo semanal.",
"RF45|Permitir registrar atividades desenvolvidas diariamente.",
"RF46|Relacionar atividade a data e participante.",
"RF47|Apresentar carga registrada junto a atividade diaria.",
"RF48|Impedir alteracao manual da carga proveniente do ponto.",
"RF49|Permitir editar atividade enquanto o periodo estiver aberto.",
"RF50|Permitir registrar resumo semanal.",
"RF51|Gerar consolidacao semanal automaticamente.",
"RF52|Apresentar carga prevista, realizada e saldo.",
"RF53|Apresentar registros diarios e atividades na consolidacao.",
"RF54|Permitir envio do relatorio semanal.",
"RF55|Permitir aprovacao pelo coordenador.",
"RF56|Permitir devolucao para correcao com observacao.",
"RF57|Permitir corrigir e reenviar relatorio devolvido.",
"RF58|Registrar data e responsavel pela aprovacao.",
"RF59|Disponibilizar dashboard individual.",
"RF60|Apresentar progresso da carga semanal.",
"RF61|Disponibilizar dashboard administrativo.",
"RF62|Exibir participantes presentes no laboratorio.",
"RF63|Exibir carga prevista e realizada por participante.",
"RF64|Identificar participantes com carga pendente.",
"RF65|Identificar atividades diarias nao preenchidas.",
"RF66|Exibir relatorios pendentes de analise.",
"RF67|Exibir ocorrencias e correcoes pendentes.",
"RF68|Consultar registros por participante e periodo.",
"RF69|Gerar relatorio semanal individual.",
"RF70|Gerar relatorio mensal individual.",
"RF71|Gerar relatorio por periodo.",
"RF72|Apresentar carga prevista e realizada nos relatorios.",
"RF73|Apresentar atividades desenvolvidas nos relatorios.",
"RF74|Apresentar resumos semanais.",
"RF75|Apresentar ocorrencias relevantes.",
"RF76|Permitir exportar relatorios em PDF."
)

$Content = "# Requisitos Funcionais`r`n`r`n"
$Content += "| ID | Requisito |`r`n"
$Content += "|---|---|`r`n"

foreach ($Requirement in $RF) {
    $Parts = $Requirement -split "\|", 2
    $Content += "| **$($Parts[0])** | $($Parts[1]) |`r`n"
}

Write-ProjectFile "docs\02-requisitos\requisitos-funcionais.md" $Content

# ============================================================
# 7. REQUISITOS NAO FUNCIONAIS
# ============================================================

$RNF = @(
"RNF01|A aplicacao web deve possuir interface responsiva.",
"RNF02|A comunicacao entre terminal e servidor devera utilizar HTTP/HTTPS.",
"RNF03|Senhas nao poderao ser armazenadas em texto puro.",
"RNF04|A API devera exigir autenticacao dos terminais RFID.",
"RNF05|O sistema devera implementar controle de acesso baseado em perfil.",
"RNF06|Operacoes administrativas relevantes deverao possuir auditoria.",
"RNF07|O terminal devera registrar temporariamente eventos durante indisponibilidade da rede.",
"RNF08|A sincronizacao nao devera produzir registros duplicados.",
"RNF09|Data e hora deverao possuir origem controlada e consistente.",
"RNF10|O sistema devera preservar integridade e rastreabilidade dos registros.",
"RNF11|O sistema devera adotar protecao adequada aos dados pessoais.",
"RNF12|O codigo-fonte devera ser versionado utilizando Git."
)

$Content = "# Requisitos Nao Funcionais`r`n`r`n"
$Content += "| ID | Requisito |`r`n"
$Content += "|---|---|`r`n"

foreach ($Requirement in $RNF) {
    $Parts = $Requirement -split "\|", 2
    $Content += "| **$($Parts[0])** | $($Parts[1]) |`r`n"
}

Write-ProjectFile "docs\02-requisitos\requisitos-nao-funcionais.md" $Content

# ============================================================
# 8. MODELO DE DOMINIO
# ============================================================

$Content = @'
# Modelo de Dominio

## Entidades principais

### Usuario

Responsavel pela autenticacao e autorizacao.

Principais atributos:

- id
- nome
- email
- senha_hash
- perfil
- ativo
- created_at
- updated_at

### Laboratorio

Representa a unidade na qual os participantes desenvolvem suas
atividades.

### Participante

Representa bolsistas e estagiarios acompanhados pelo sistema.

### TipoVinculo

Define regras gerais para tipos de participantes, como Bolsista e
Estagiario.

### Vinculo

Relaciona um participante a determinado tipo de vinculo em um periodo.

### Projeto

Representa projetos ou atividades aos quais os participantes podem
estar associados.

### CartaoRFID

Representa o identificador fisico utilizado pelo participante.

### Terminal

Representa um equipamento ESP32/RFID instalado no laboratorio.

### Programacao

Define a programacao semanal vigente de um participante.

### ProgramacaoDia

Define horarios e carga prevista para cada dia da programacao.

### EventoRFID

Representa o evento bruto recebido do terminal.

O evento bruto deve ser preservado independentemente da interpretacao
posterior realizada pelo sistema.

### RegistroPonto

Representa a interpretacao de um evento de frequencia.

Tipos previstos:

- ENTRADA
- SAIDA_INTERVALO
- RETORNO_INTERVALO
- SAIDA

### JornadaDiaria

Consolida carga prevista, realizada e saldo de determinado dia.

Duracoes deverao preferencialmente ser armazenadas em minutos.

### AtividadeDiaria

Contem a descricao das atividades desenvolvidas pelo participante em
determinado dia.

A carga horaria nao sera digitada manualmente. Ela sera obtida da
jornada calculada.

### RelatorioSemanal

Consolida:

- carga prevista;
- carga realizada;
- saldo;
- atividades;
- resumo semanal;
- situacao da analise.

### EventoCalendario

Representa:

- feriado;
- recesso;
- suspensao.

### Afastamento

Representa periodos individuais nos quais o participante fica
dispensado das atividades.

### Justificativa

Representa justificativas de ausencia.

### SolicitacaoAjuste

Representa pedidos de correcao de registros de ponto.

### Auditoria

Mantem historico das operacoes administrativas relevantes.

## Relacionamentos gerais

```text
USUARIO
   |
   +-- PARTICIPANTE
          |
          +-- VINCULO ---- TIPO_VINCULO
          |
          +-- CARTAO_RFID
          |       |
          |       +-- EVENTO_RFID ---- TERMINAL
          |
          +-- PROGRAMACAO
          |       |
          |       +-- PROGRAMACAO_DIA
          |
          +-- REGISTRO_PONTO
          |       |
          |       +-- JORNADA_DIARIA
          |               |
          |               +-- ATIVIDADE_DIARIA
          |
          +-- RELATORIO_SEMANAL
          +-- JUSTIFICATIVA
          +-- SOLICITACAO_AJUSTE
          +-- AFASTAMENTO

LABORATORIO
   |
   +-- PROJETO
   +-- TERMINAL
   +-- EVENTO_CALENDARIO
Principio de rastreabilidade

O CheckPonto deve separar:

evento observado pelo hardware;
interpretacao do evento;
consolidacao da jornada.

Assim, EVENTO_RFID representa o fato bruto e imutavel recebido do
terminal, enquanto REGISTRO_PONTO representa sua classificacao dentro
da jornada.
'@

Write-ProjectFile "docs\04-banco-dados\modelo-dominio.md" $Content

============================================================
9. VALIDACAO
============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host " VALIDACAO"
Write-Host "============================================================"
Write-Host ""

$Files = @(
"docs\01-visao\visao-geral.md",
"docs\01-visao\escopo.md",
"docs\01-visao\atores.md",
"docs\02-requisitos\regras-negocio.md",
"docs\02-requisitos\requisitos-funcionais.md",
"docs\02-requisitos\requisitos-nao-funcionais.md",
"docs\04-banco-dados\modelo-dominio.md"
)

$Errors = 0

foreach ($File in $Files) {

$Path = Join-Path $Root $File

if ((Test-Path $Path) -and ((Get-Item $Path).Length -gt 0)) {
    $Size = (Get-Item $Path).Length
    Write-Host "[OK] $File ($Size bytes)"
}
else {
    Write-Host "[ERRO] $File"
    $Errors++
}

}

Write-Host ""

if ($Errors -eq 0) {
Write-Host "============================================================"
Write-Host " DOCUMENTACAO INICIAL CONFIGURADA COM SUCESSO"
Write-Host "============================================================"
}
else {
Write-Host "[ERRO] Foram encontrados $Errors problema(s)."
exit 1
}

Write-Host ""


Execute **da raiz `C:\Users\renato\Documents\CheckPonto`**:

.\scripts\setup\01_configurar_documentacao.ps1