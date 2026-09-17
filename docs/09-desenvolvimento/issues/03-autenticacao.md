# Issue 03 — [AUTH] Implementar autenticação e perfis

## Objetivo
Permitir acesso autenticado de coordenadores e participantes.

## Escopo
- login por usuário/senha;
- armazenamento seguro de senha;
- sessão/token;
- middleware de autenticação;
- autorização por perfil;
- endpoint `/auth/me`;
- tela de login.

## Requisitos relacionados
- RF01, RF03, RF04, RF05
- RNF03, RNF05
- UC01
- CT21

## Critérios de aceitação
- [ ] credenciais válidas autenticam;
- [ ] credenciais inválidas são rejeitadas;
- [ ] senha não fica em texto puro;
- [ ] rotas protegidas exigem autenticação;
- [ ] participante não acessa dados privados de terceiros;
- [ ] frontend trata sessão e logout.

## Dependências
- Issue 01
- Issue 02

## Testes esperados
Login válido, login inválido, rota sem token e permissão por perfil.
