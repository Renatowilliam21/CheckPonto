# Issue 01 — [BASE] Estruturar aplicação backend Node.js + TypeScript

## Objetivo
Criar a fundação técnica da API REST do CheckPonto.

## Escopo
- iniciar projeto Node.js + TypeScript em `backend/`;
- organizar `routes`, `controllers`, `services`, `repositories`, `validators` e `middlewares`;
- configurar variáveis de ambiente;
- preparar acesso ao PostgreSQL;
- criar endpoint de health check;
- documentar execução local.

## Referências
- RNF02, RNF03, RNF05, RNF10, RNF12
- `docs/03-arquitetura/`
- `docs/05-api/`

## Critérios de aceitação
- [ ] backend inicia sem erros;
- [ ] TypeScript configurado;
- [ ] estrutura segue a arquitetura;
- [ ] endpoint de saúde disponível;
- [ ] nenhuma credencial real versionada;
- [ ] README do backend atualizado;
- [ ] alteração enviada por Pull Request.

## Testes esperados
- inicialização da aplicação;
- resposta do health check;
- tratamento de configuração ausente.

## Dependências
Nenhuma.

## Fora do escopo
Autenticação e regras de negócio.
