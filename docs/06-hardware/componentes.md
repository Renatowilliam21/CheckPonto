# Componentes de Hardware — CheckPonto

## Objetivo do terminal

O terminal RFID registra eventos físicos de aproximação de cartão e os envia
para a API do CheckPonto.

O terminal não deve decidir regras complexas de jornada.

## Componentes previstos

### ESP32

Microcontrolador responsável por:

- conexão Wi-Fi;
- leitura do RFID;
- geração do identificador do evento;
- obtenção de data/hora;
- envio para API;
- feedback ao usuário;
- armazenamento temporário offline.

### RC522

Leitor RFID utilizado para obter o UID do cartão.

### Cartões ou tags RFID

Identificadores físicos dos participantes.

### LEDs

Feedback simples:

- leitura detectada;
- sucesso;
- erro;
- operação offline.

### Buzzer

Feedback sonoro opcional.

### Display OLED

Componente opcional para apresentar mensagens como:

- cartão lido;
- registro recebido;
- sem conexão;
- sincronizando.

### RTC DS3231

Componente recomendado para manter referência temporal quando o terminal
estiver temporariamente sem acesso à rede.

## Observação

A lista é uma proposta de referência. A equipe de hardware deverá confirmar
os componentes disponíveis antes de fixar pinagem e montagem definitiva.
