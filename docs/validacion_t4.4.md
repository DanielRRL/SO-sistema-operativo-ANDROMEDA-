# Validación T4.4 — Recorrido completo

- **Tarea:** T4.4
- **Fase:** 4. Integración
- **Responsable:** Todos; validación de la parte de A
- **Depende de:** T4.1, T4.2, T4.3
- **Estado:** Validado por A; pendiente confirmación conjunta de B, C y D

## 1. Objetivo

Ejecutar la sesión de ejemplo completa del simulador y comprobar que procesos,
memoria, planificación, estadísticas, archivos, concurrencia y mensajes
funcionan juntos sin errores técnicos.

## 2. Entorno

- Linux.
- Python 3.14.4 (compatible con el requisito de Python 3.10+).
- Rama `persona-a` sincronizada con `main`.

## 3. Comandos ejecutados

```bash
python3 -m unittest discover -s pruebas -v
python3 main.py --script pruebas/demo.txt
```

## 4. Resultados

- **155 pruebas unitarias:** todas correctas.
- **Script de demo:** termina con código 0 y sin `Traceback`.
- **Archivos:** la demo crea, lista, lee, modifica y elimina `notas.txt` dentro
  de `carpeta_pruebas`; la carpeta queda vacía al terminar.
- **Errores esperados:**
  - `memoria asignar 1 2000` responde `[ERROR]` por superar los 1024 MB.
  - `crear editor cpu=8` responde `[ERROR]` por faltar la palabra `proceso`.
  - `concurrencia sin_lock` puede responder `[ERROR]` porque la condición de
    carrera se detectó; `con_lock` y `semaforo` responden `[OK]`.

## 5. Validación de la parte de A

| Caso | Resultado observado |
|---|---|
| `ejemplo` | Carga P1–P4 con llegada, CPU, prioridad y memoria correctas. |
| `listar procesos` / `consultar proceso 2` | Tablas correctas. |
| `planificar fcfs` | Gantt `0-8, 8-12, 12-21, 21-26`; promedios `15.25 / 8.75`. |
| `planificar sjf` | Gantt `0-8, 8-12, 12-17, 17-26`; promedios `14.25 / 7.75`. |
| `planificar rr quantum=3` | Gantt de 10 segmentos; promedios `20.00 / 13.50`. |
| `estadisticas` | Coincide con el resultado de la última planificación. |
| `memoria estado` | 548 MB usados con P1–P4. |
| `memoria asignar 1 2000` | Rechazado; no altera la memoria. |
| `finalizar proceso 1` | Libera 128 MB; quedan 420 MB usados. |

## 6. Evidencias

- [`docs/evidencias/simulador/`](./evidencias/simulador/)
- [`docs/comparacion_simulacion_linux.md`](./comparacion_simulacion_linux.md)
- [`pruebas/demo.txt`](../pruebas/demo.txt)

## 7. Conclusión

La parte de A del recorrido completo está validada y no requirió correcciones.
Falta que B, C y D confirmen sus módulos para cerrar T4.4 como equipo y avanzar
a T5.5/T5.6.
