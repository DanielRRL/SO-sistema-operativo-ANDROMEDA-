# Guion de la Demo — T7.1

- **Tarea:** T7.1
- **Fase:** 7. Sustentación
- **Responsable:** Todos; preparación de A
- **Depende de:** T6.5, T6.1
- **Duración objetivo:** 20–22 minutos
- **Estado:** Guion preparado; faltan los dos ensayos con el equipo

## 1. Preparación

Antes de la demo:

```bash
python3 -m unittest discover -s pruebas -v
python3 main.py
```

Comprobar:

- 155 pruebas correctas.
- Consola con prompt `simulador> `.
- `carpeta_pruebas/` vacía al inicio.
- Terminal con fuente legible y tamaño adecuado.

Si se usa el modo automático:

```bash
python3 main.py --script pruebas/demo.txt
```

## 2. Reparto de roles

| Persona | Módulos que presenta |
|---|---|
| A | Procesos, FCFS, SJF, Round Robin, estadísticas y memoria-procesos |
| B | Lexer, tokens, memoria y archivos |
| C | Parser, despachador, consola, mensajes y modo script |
| D | Hilos, Lock/Semaphore, prácticas Linux y comparación |

Todos deben poder responder por el módulo de otro. Las preguntas cruzadas se
preparan en la sección 5.

## 3. Guion por bloques

### 0:00–2:00 — Introducción y arquitectura (A/C)

Comandos:

```text
ayuda
```

Qué decir:

- ANDROMEDA es un simulador de SO por línea de comandos, sin GUI.
- Flujo: `main.py → lexer → parser → consola → módulo → [OK]/[ERROR]`.
- Todo usa Python 3.10+ y biblioteca estándar.
- Mostrar el diagrama modular de `docs/diagrama_modular.md`.

### 2:00–5:00 — Lexer y tokens (B)

Comandos:

```text
ayuda planificar
tokens crear proceso editor llegada=0 cpu=8
```

Qué decir:

- El lexer reconoce 36 palabras reservadas, identificadores, números, cadenas,
  nombres de archivo, `=` y comentarios.
- Cada token guarda tipo, lexema, línea y columna.
- Los errores se reportan como `ERROR` sin detener el análisis.
- El comando `tokens` es la forma directa de demostrar el lexer.

### 5:00–7:00 — Parser y consola (C)

Comandos:

```text
crear editor cpu=8
```

Qué decir:

- El parser valida la gramática de T1.2 y construye una `Orden`.
- Si falta la palabra `proceso`, responde `[ERROR]` con el uso correcto.
- El despachador conecta la orden con el módulo correspondiente.
- El programa nunca muestra un traceback por una entrada inválida.

### 7:00–12:00 — Procesos, planificación y estadísticas (A)

Comandos:

```text
ejemplo
listar procesos
consultar proceso 2
planificar fcfs
estadisticas
planificar sjf
estadisticas
planificar rr quantum=3
estadisticas
```

Qué decir:

- P1–P4 tienen llegada, CPU, prioridad y memoria.
- FCFS: `15.25 / 8.75` de retorno/espera.
- SJF: `14.25 / 7.75`; reduce la espera porque ejecuta primero el trabajo corto.
- RR: `20.00 / 13.50`; reparte la CPU, pero aumenta el retorno.
- Los planificadores no mutan los procesos y solo consideran `LISTO`.
- Mostrar el Gantt y la tabla de estadísticas.

### 12:00–15:00 — Memoria y archivos (B)

Comandos:

```text
memoria estado
memoria asignar 1 2000
finalizar proceso 1
memoria estado
archivo crear notas.txt "primera linea"
archivo listar
archivo leer notas.txt
archivo modificar notas.txt "segunda linea"
archivo eliminar notas.txt
```

Qué decir:

- La memoria tiene 1024 MB; P1–P4 consumen 548 MB.
- Pedir 2000 MB falla por capacidad.
- Al finalizar P1 se liberan 128 MB.
- Los archivos solo se crean dentro de `carpeta_pruebas/`; se rechazan rutas con
  `..` o rutas absolutas.

### 15:00–18:00 — Concurrencia y Linux (D)

Comandos:

```text
concurrencia sin_lock
concurrencia con_lock
concurrencia semaforo
```

Qué decir:

- `sin_lock` puede mostrar `[ERROR]` porque se detecta la condición de carrera.
- `con_lock` y `semaforo` muestran `[OK]` con el valor esperado.
- Relacionar con `threading`, sección crítica y las prácticas de Linux.
- Mostrar las capturas de `docs/evidencias/linux/` y la comparación de
  `docs/comparacion_simulacion_linux.md`.

### 18:00–20:00 — Mensajes, script y errores (C)

Comandos:

```text
mensaje enviar "hola"
mensaje recibir
```

Qué decir:

- La cola es FIFO y segura entre hilos.
- El modo `--script` ejecuta la misma sesión desde un archivo.
- Los errores de sintaxis, memoria, archivos y pid inexistente se muestran con
  `[ERROR]` y explicación.

### 20:00–22:00 — Cierre (Todos)

Qué decir:

- Cada integrante menciona una dificultad y lo aprendido.
- Recordar que el proyecto usa solo biblioteca estándar y Linux.
- Preguntas del docente.

## 4. Ensayos realizados

Se ejecutó la demo completa dos veces en local:

```bash
python3 main.py --script pruebas/demo.txt
```

| Ensayo | Resultado | Tiempo de ejecución | Traceback |
|---|---|---:|---|
| 1 | Código 0 | 0.74 s | Ninguno |
| 2 | Código 0 | 0.74 s | Ninguno |

La carpeta `carpeta_pruebas/` quedó vacía después de ambas ejecuciones. El tiempo
de 0.74 s corresponde solo al script; la narración y las preguntas completan los
20–22 minutos.

## 5. Preguntas cruzadas para ensayar

- ¿Qué diferencia hay entre lexer y parser?
- ¿Qué es un token, un lexema y una columna?
- ¿Por qué `NOMBRE_ARCHIVO` se reconoce antes que `ID` y `NUMERO`?
- ¿Por qué `crear` produce el mismo token en `crear proceso` y `archivo crear`?
- ¿Cómo se decide entre FCFS, SJF y RR?
- ¿Por qué los planificadores no deben modificar los procesos?
- ¿Qué ocurre si se pide más memoria de la disponible?
- ¿Cómo se evita que un archivo salga de `carpeta_pruebas/`?
- ¿Qué diferencia hay entre `Lock` y `Semaphore(1)`?
- ¿Qué garantiza una cola FIFO de mensajes?
- ¿Qué pasa si el usuario escribe un comando mal formado?

## 6. Pendiente para cerrar T7.1

- Ensayo 1 con cronómetro y reparto real de roles.
- Ensayo 2 con preguntas cruzadas.
- Ajustar tiempos si el docente asigna menos de 20 minutos.
