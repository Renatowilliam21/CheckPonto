# Guia de Desenvolvimento para os Alunos

## 1. Antes de programar

Todos devem conhecer:

1. `README.md`;
2. `docs/01-visao/`;
3. `docs/02-requisitos/`;
4. `docs/03-arquitetura/`;
5. documentação do módulo em que trabalharão.

Não iniciar pela criação de telas sem compreender o fluxo de negócio.

## 2. Organização técnica

```text
frontend/       aplicação web
backend/        API e regras de negócio
database/       banco e modelo
firmware/       ESP32/RFID
infrastructure/ infraestrutura
tests/          testes globais
docs/           documentação
```

## 3. Fluxo de trabalho

```text
Issue
  -> Branch
      -> Implementação
          -> Testes
              -> Commit
                  -> Push
                      -> Pull Request
                          -> Revisão
                              -> main
```

## 4. Branches

Exemplos:

```text
feature/login
feature/cadastro-participante
feature/programacao-semanal
feature/leitura-rfid
feature/registro-atividade
fix/evento-rfid-duplicado
docs/protocolo-rfid
```

Não desenvolver diretamente na `main`.

## 5. Commits

Padrão sugerido:

```text
feat: adiciona cadastro de participantes
fix: corrige calculo da jornada diaria
docs: atualiza protocolo RFID
test: adiciona teste de evento duplicado
refactor: reorganiza servico de ponto
chore: ajusta configuracao do projeto
```

## 6. Pull Request

O PR deve informar:

- o que foi desenvolvido;
- requisito relacionado;
- como testar;
- evidências quando aplicável;
- limitações conhecidas.

## 7. Definição de pronto

Uma tarefa está pronta quando:

- atende ao requisito;
- respeita a arquitetura;
- possui validações;
- possui tratamento básico de erro;
- foi testada;
- não contém segredos;
- documentação afetada foi atualizada;
- passou por revisão.

## 8. Regra importante

O projeto deve crescer incrementalmente.

Evitar implementar muitos módulos incompletos ao mesmo tempo.
