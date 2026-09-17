# Pinagem — Terminal RFID

## Situação

A pinagem definitiva ainda não está congelada.

Isso é intencional: os alunos devem confirmar o modelo exato da placa ESP32,
do RC522 e dos componentes adicionais disponíveis no laboratório.

## RC522

O RC522 normalmente será utilizado via SPI.

Sinais necessários:

| Sinal | Função |
| --- | --- |
| SDA/SS | seleção SPI |
| SCK | clock |
| MOSI | dados ESP32 -> RC522 |
| MISO | dados RC522 -> ESP32 |
| RST | reset |
| 3.3V | alimentação |
| GND | terra |

## Regra importante

O RC522 deve operar com alimentação e níveis lógicos adequados ao módulo.
A montagem deverá ser conferida antes da energização.

## Antes de definir GPIOs

A equipe deverá:

1. identificar o modelo exato do ESP32;
2. verificar GPIOs reservados ou problemáticos;
3. verificar SPI disponível;
4. considerar OLED, buzzer, LEDs e RTC;
5. documentar a decisão;
6. atualizar esta página.

Não copiar pinagem de outro projeto sem conferir a placa utilizada.
