# Como Contribuir com o CheckPonto

## Fluxo

1. selecionar uma Issue;
2. criar branch;
3. desenvolver;
4. testar;
5. atualizar documentação quando necessário;
6. realizar commits claros;
7. enviar branch;
8. abrir Pull Request;
9. corrigir observações da revisão;
10. integrar somente após aprovação.

## Branch

Não trabalhar diretamente na `main`.

## Commits

Use mensagens objetivas, por exemplo:

```text
feat: adiciona cadastro de participantes
fix: evita duplicidade de evento RFID
docs: atualiza fluxo de jornada
test: adiciona teste de intervalo
```

## Pull Requests

Todo PR deve indicar requisito, mudança realizada e forma de teste.

## Segurança

Nunca versionar:

- senhas;
- tokens;
- chaves de API;
- credenciais de banco;
- arquivos `.env` reais.

## Documentação

Mudanças no comportamento do sistema devem atualizar a documentação
correspondente.
