# Issue 09 — [RFID] Implementar cadastro e autenticação de terminais

## Objetivo
Permitir que somente terminais autorizados enviem eventos RFID.

## Requisitos relacionados
- RF15, RF17
- RNF04
- UC06

## Escopo
- cadastrar terminal;
- identificar `device_id`;
- gerar/administrar credencial;
- armazenar somente representação segura da credencial;
- autenticar requisições do terminal.

## Critérios de aceitação
- [ ] terminal cadastrado possui identificador único;
- [ ] terminal autorizado envia requisição;
- [ ] terminal não autorizado é rejeitado;
- [ ] segredo não é armazenado em texto puro quando aplicável;
- [ ] logs não expõem segredo.

## Dependências
Issue 01.

## Testes esperados
Terminal válido, inválido e credencial ausente.
