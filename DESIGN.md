# Triage Queue — Design Notes

## Estructura de datos

La cola utiliza `heapq` de la biblioteca estándar de Python.

Cada paciente se almacena como `(triage_level, arrival_sequence, patient)`. Esto garantiza que los pacientes de nivel 1 se atiendan antes que los de nivel 2, y los de nivel 2 antes que los de nivel 3. El contador `arrival_sequence` conserva FIFO entre pacientes con el mismo nivel de triaje.

Elegí `heapq` porque una sola `deque` obligaría a buscar o reordenar posiciones al insertar pacientes críticos. Tres colas separadas también serían válidas, pero `heapq` mantiene prioridad y FIFO en una sola estructura.

## Operaciones

- `enqueue(patient)`: añade un paciente respetando prioridad y FIFO.
- `dequeue()`: extrae al siguiente paciente.
- `peek()`: devuelve al siguiente paciente sin retirarlo.
- `list_queue()`: devuelve todos los pacientes en orden de atención.
- `stats()`: devuelve la cantidad de pacientes por nivel de triaje.

`dequeue()` y `peek()` lanzan un `IndexError` descriptivo cuando la cola está vacía.

## Concurrencia

Este proyecto es una aplicación CLI de un solo proceso y no implementa concurrencia real.

En producción, si un worker extrae un paciente mientras otro agrega un paciente crítico, las mutaciones de la cola deben ser atómicas. El orden recomendado es:

1. Adquirir un lock o iniciar una transacción.
2. Seleccionar y retirar al paciente de mayor prioridad.
3. Marcarlo como `processing`.
4. Confirmar el cambio.
5. Liberar el lock o cerrar la transacción.

El worker que agrega pacientes debe usar el mismo límite de sincronización. Así se evita que dos workers procesen al mismo paciente o que lean un estado parcial.
