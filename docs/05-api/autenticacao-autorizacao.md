# Autenticação e Autorização

## Perfis iniciais

### COORDENADOR
Administra os recursos do laboratório e analisa pendências.

### PARTICIPANTE
Consulta os próprios dados, registra atividades, envia relatórios,
justificativas e solicitações de ajuste.

## Terminal RFID

O terminal não utiliza credenciais de usuário.

Cada terminal deverá possuir uma credencial própria. O servidor armazena
somente uma representação segura dessa credencial.

## Princípios

- senha nunca armazenada em texto puro;
- autorização validada no backend;
- participante não acessa dados individuais de terceiros;
- operações administrativas relevantes são auditadas;
- credenciais e segredos não são versionados no Git.
