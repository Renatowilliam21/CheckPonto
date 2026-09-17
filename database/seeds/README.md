# Seeds — CheckPonto

## 001_tipos_vinculo.sql

Cria os tipos iniciais:

- BOLSISTA;
- ESTAGIARIO.

Para BOLSISTA:

- carga semanal padrão: 960 minutos = 16 horas;
- carga diária mínima de referência: 240 minutos = 4 horas;
- carga diária máxima de referência: 360 minutos = 6 horas.

Para ESTAGIARIO:

- a carga semanal padrão permanece 0 porque deve ser definida no vínculo;
- carga diária mínima de referência: 240 minutos = 4 horas;
- carga diária máxima de referência: 480 minutos = 8 horas.

Os valores são parâmetros iniciais e poderão ser alterados pela aplicação
sem modificar o firmware.
