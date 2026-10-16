# Notas

## Observación pendiente (no corregida)
`seed.py` usa `INSERT OR IGNORE`, así que volver a ejecutarlo no restaura los estados modificados durante las pruebas. Para reiniciar los datos hay que borrar `data/orders.sqlite3` y ejecutar `python seed.py`.
No lo cambié para no alterar el comportamiento esperado del seed (no duplicar pedidos). Propuesta: agregar una opción `--reset` que recree la tabla.

## Uso de IA
Usé Claude Code como mentor técnico durante todo el ejercicio, este me ayudó a estructurar el análisis y a identificar los errores, y propuso el código de la solución.

Mi trabajo fue entender y validar cada propuesta recibida,  leí el código para confirmar la causa del bug, lo reproduje antes de corregirlo y verifiqué la solución con `curl` y en el navegador, incluido el caso de dos pestañas enviando el mismo pedido.

También cuestioné algunas decisiones antes de aceptarlas luego de entenderlas bien las acepté o corregí. 