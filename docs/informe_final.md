# Informe final: Simulador de Sistema Operativo ANDROMEDA

- **Espacio académico:** Sistemas Operativos, Ingeniería de Software
- **Tarea:** T6.4
- **Versión evaluada:** `main` del repositorio (Python 3.10 o superior, solo biblioteca estándar)

## 1. Resumen

ANDROMEDA es un simulador didáctico de un sistema operativo, con interfaz de consola en Python.
Permite crear, consultar y finalizar procesos; planificarlos con FCFS, SJF no expulsivo y Round
Robin; calcular estadísticas; simular memoria; operar archivos de forma segura; demostrar
concurrencia y sincronización con hilos; y usar una cola de mensajes. Se complementó con
prácticas en Linux (procesos, prioridades, hilos y permisos) y con una comparación entre el
modelo programado y el sistema real.

## 2. Cumplimiento de los requerimientos

| Módulo del enunciado | Requerimiento | Implementación |
|---|---|---|
| Procesos | Identificador, nombre, llegada, CPU, prioridad, memoria y estado | `procesos.py` (clase `Proceso`, 5 estados) |
| Planificación | FCFS, SJF no expulsivo y Round Robin | `planificador.py` |
| Estadísticas | Finalización, retorno, espera y promedios | `estadisticas.py` |
| Concurrencia | Al menos dos hilos sobre un recurso compartido | `hilos_sync.py` (4 hilos, contador compartido) |
| Sincronización | Proteger la sección crítica con Lock o Semaphore y explicar | `hilos_sync.py` (`con_lock`, `semaforo`) |
| Comunicación | Cola de mensajes | `mensajes.py` (FIFO) |
| Memoria | Asignar y liberar validando la capacidad | `memoria.py` (1024 MB) |
| Archivos | Crear, listar, leer, modificar y eliminar en una carpeta de pruebas | `archivos.py` (`carpeta_pruebas/`) |
| Linux | Prácticas de procesos, prioridades, hilos y permisos | `docs/evidencias/linux/` |

La consola integra todos los módulos mediante `main.py`, `lexer.py`, `parser.py` y
`consola.py`. La arquitectura y los diagramas están en `docs/diagrama_modular.md`.

## 3. Pruebas

### 3.1 Pruebas unitarias

Se usó `unittest` de la biblioteca estándar. Resultado: **155 pruebas, todas correctas**.

```bash
python3 -m unittest discover -s pruebas -v
```

| Archivo | Pruebas | Qué cubre |
|---|---|---|
| `test_lexer.py` | 30 | Tokens, cadenas, comentarios, errores léxicos, línea y columna |
| `test_parser.py` | 32 | Gramática de todos los comandos y mensajes de uso |
| `test_planificador.py` | 21 | FCFS, SJF y RR con los datos de ejemplo |
| `test_algoritmos_borde.py` | 8 | Un solo proceso, CPU libre y quantum 1 |
| `test_procesos.py` | 12 | Ciclo de vida, validaciones y estados |
| `test_estadisticas.py` | 7 | Tiempos, promedios y formato |
| `test_integracion_memoria.py` | 8 | Reserva, rechazo y liberación al finalizar |
| `test_persona_b.py` | 14 | Memoria y archivos |
| `test_hilos_sync.py` | 9 | Los tres modos de concurrencia y sus errores |
| `test_mensajes.py` | 7 | Cola FIFO |
| `test_errores.py` | 7 | Entradas inválidas sin errores técnicos |

### 3.2 Prueba de extremo a extremo

Se ejecutó la sesión completa de ejemplo:

```bash
python3 main.py --script pruebas/demo.txt
```

El script termina con código 0 y sin ningún `Traceback`. Se guardaron 10 capturas con su
explicación en `docs/evidencias/simulador/`. Las entradas inválidas probadas devuelven un
mensaje `[ERROR]` con el motivo y el uso correcto:

| Entrada | Resultado |
|---|---|
| `crear editor cpu=8` | `[ERROR]` indicando que faltaba la palabra `proceso` y la columna |
| `finalizar proceso 99` | `[ERROR] No existe el proceso 99.` |
| `memoria asignar 1 2000` | `[ERROR]` por superar la capacidad de 1024 MB |
| `archivo leer ../secreto.txt` | `[ERROR]` por carácter no reconocido; no se lee fuera de `carpeta_pruebas` |

### 3.3 Revisión cruzada de código

| Revisión | Estado | Resultado |
|---|---|---|
| A revisa a B | Aprobada | Sin defectos bloqueantes (`docs/revision_cruzada_A_B.md`) |
| B revisa a C | Aprobada | Revisó `parser.py`, `consola.py` y `main.py`; 155 pruebas y demo correctas, sin defectos bloqueantes. Observación: actualizar una nota del README sobre el despacho de comandos (resuelta). |
| C revisa a D | _Pendiente de reporte_ | |
| D revisa a A | _Pendiente de reporte_ | |

## 4. Resultados

### 4.1 Planificación

Se ejecutaron los tres algoritmos sobre los cuatro procesos de ejemplo.

| Proceso | Llegada | CPU | Prioridad | Memoria (MB) |
|---|---|---|---|---|
| P1 | 0 | 8 | 2 | 128 |
| P2 | 1 | 4 | 1 | 64 |
| P3 | 2 | 9 | 3 | 256 |
| P4 | 3 | 5 | 2 | 100 |

| Algoritmo | Diagrama de Gantt | Promedio retorno | Promedio espera |
|---|---|---|---|
| FCFS | P1 [0-8], P2 [8-12], P3 [12-21], P4 [21-26] | 15,25 | 8,75 |
| SJF no expulsivo | P1 [0-8], P2 [8-12], P4 [12-17], P3 [17-26] | 14,25 | 7,75 |
| Round Robin (q=3) | P1, P2, P3, P4, P1, P2, P3, P4, P1, P3 | 20,00 | 13,50 |

**Análisis:** SJF obtiene los mejores promedios porque atiende primero a los procesos cortos,
a costa de que P3 espere 15 unidades. FCFS es simple pero penaliza a los procesos que llegan
detrás de uno largo. Round Robin da los promedios más altos por los cambios de turno, pero
reparte la CPU de forma equitativa y evita que un proceso largo monopolice el procesador.

### 4.2 Memoria

Con los cuatro procesos cargados hay 548 MB usados y 476 MB libres de 1024 MB. Pedir 2000 MB
devuelve `[ERROR]` sin alterar la memoria. Al finalizar el proceso 1 se liberan 128 MB y
quedan 420 MB usados y 604 MB libres. Un proceso que no cabe queda en estado `RECHAZADO`.

### 4.3 Concurrencia y sincronización

Cuatro hilos incrementan 1000 veces un contador compartido; el valor esperado es 4000.

| Modo | Resultado | Explicación |
|---|---|---|
| `sin_lock` | Aprox. 1000 de 4000 (varía en cada ejecución) | Condición de carrera: los hilos leen el mismo valor y se sobrescriben los incrementos |
| `con_lock` | 4000 de 4000 | `threading.Lock` deja entrar a un solo hilo a la sección crítica |
| `semaforo` | 4000 de 4000 | `threading.Semaphore(1)` produce el mismo efecto |

### 4.4 Archivos y mensajes

Se probó el ciclo completo de archivos dentro de `carpeta_pruebas/` (crear, listar, leer,
modificar con agregado al final, y eliminar). Las rutas con `..`, absolutas y los enlaces se
rechazan. La cola de mensajes entrega los mensajes en orden de llegada.

### 4.5 Prácticas en Linux y comparación

Se realizaron las cuatro prácticas con 16 capturas (`docs/evidencias/linux/`):

| Práctica | Observación principal |
|---|---|
| Procesos | Cada proceso tiene PID y PPID; los procesos forman un árbol cuya raíz es `systemd` |
| Prioridades | `renice -n 19` subió el valor nice de 5 a 19 y bajó `PRI` de 14 a 0; bajar el nice por debajo de lo permitido da "Permiso denegado" sin `sudo` |
| Hilos | Todos los hilos de un proceso comparten el PID y la memoria; un programa Python con 4 hilos muestra 5 en `NLWP` |
| Permisos | Con `chmod 200` ni el dueño pudo leer el archivo; un script sin permiso `x` no se ejecuta |

La tabla completa de diferencias está en `docs/comparacion_simulacion_linux.md`. Las más
relevantes: en el simulador la prioridad es solo un dato y los algoritmos no la usan, mientras
que en Linux sí cambia el reparto de CPU; el simulador modela la memoria como un tope fijo y
Linux distingue memoria virtual y física; y el simulador protege archivos confinándolos a una
carpeta, mientras que Linux lo hace con permisos por usuario, grupo y otros.

## 5. Dificultades

**Persona A (núcleo, planificación y estadísticas):**
Lo más difícil fue coordinar el trabajo en ramas paralelas y resolver conflictos en `main.py`,
`consola.py` y `tokens.py` sin perder lo ya integrado. También tuvimos que unificar dos
sintaxis propuestas, T1.1 y T1.2, y ajustar lexer, parser, pruebas y documentación. Integrar
procesos, memoria y planificación exigió cuidar estados, rechazos por capacidad y que los
planificadores no mutaran los procesos. Finalmente, pasar de pruebas básicas a 155 casos y
cubrir errores de consola, CPU ociosa y quantum 1 tomó tiempo, pero evitó regresiones en la
demo.

**Persona B (lexer, memoria y archivos):**
En el lexer fue necesario probar distintos casos, como cadenas con comillas, nombres de
archivo y caracteres no reconocidos. En la gestión de memoria hubo que cuidar que las reservas
respetaran el límite de 1024 MB y que al finalizar procesos se liberara la memoria
correspondiente. En las operaciones de archivos se validaron las rutas para evitar que las
acciones salieran de `carpeta_pruebas`. La integración requirió ejecutar la demo y ajustar
las pruebas para distinguir errores intencionales de fallos reales.

**Dificultades de integración y robustez (aporte del equipo):**
Una de las principales dificultades fue construir el lexer y el parser desde cero, sin
librerías externas, lo que exigió definir con precisión la tabla de terminales, la gramática y
el reporte de errores con línea y columna. También fue complejo integrar los módulos entre sí
(memoria-procesos, despachador y planificadores), porque cada uno manejaba contratos y
estructuras de datos propias que debían coincidir. En concurrencia, reproducir de forma visible
la condición de carrera y demostrar el efecto de Lock y Semaphore requirió ajustar los hilos
para que el resultado fuera estable y didáctico. Por último, garantizar que ninguna entrada
inválida tumbara el programa obligó a probar casos límite de forma sistemática y a unificar el
formato de mensajes `[OK]` y `[ERROR]`.

**Persona D (concurrencia, Linux y documentación):**
En la concurrencia, la condición de carrera casi no aparece en versiones recientes de Python
con un simple `contador += 1`, porque el intérprete cambia de hilo pocas veces. Se separó la
lectura de la escritura del contador y se cedió el procesador entre ambas con `time.sleep(0)`.
El primer intento con `Event().wait(0)` no cedía el procesador y las pruebas fallaban. En las
prácticas de Linux hubo que repetir cuatro capturas: una no mostraba el proceso de prueba, otra
mostraba un error porque el proceso ya había terminado, una no cambiaba la prioridad porque la
terminal ya tenía un valor nice distinto de 0, y una usaba una variable que quedó vacía. Esto
obligó a revisar cada captura contra lo que debía demostrar. En la documentación, los diagramas
se regeneraron al final con las dependencias reales del código, verificadas contra los `import`.

## 6. Conclusiones

1. El simulador cumple los requerimientos funcionales del enunciado: procesos, planificación
   con tres algoritmos, estadísticas, memoria, archivos, concurrencia con Lock y Semaphore, y
   cola de mensajes, todo integrado en una consola con manejo de errores sin tracebacks.
2. La planificación mostró el compromiso entre algoritmos: SJF minimiza los tiempos promedio
   (14,25 de retorno y 7,75 de espera), FCFS es el más simple y Round Robin prioriza la
   equidad a costa de promedios mayores (20,00 y 13,50).
3. La demostración de concurrencia confirma que compartir datos sin protección pierde
   actualizaciones y que un Lock o un Semaphore garantizan un resultado exacto.
4. La comparación con Linux muestra que el simulador es una versión reducida y controlada del
   sistema real: modela bien el ciclo de vida de los procesos, la planificación y la
   sincronización, pero simplifica la prioridad, la memoria y los permisos.
5. El trabajo por contratos y stubs (firmas acordadas al inicio, módulos reemplazables) permitió
   que cuatro personas desarrollaran en paralelo e integraran sin reescribir. Las 155 pruebas y
   las revisiones cruzadas dieron confianza para integrar.
6. Como mejoras futuras: usar la prioridad en un cuarto algoritmo, mostrar los estados
   `EJECUTANDO` durante la planificación y permitir reutilizar el nombre de un proceso ya
   terminado.

## Anexo: ubicación de las evidencias

| Contenido | Ruta |
|---|---|
| Diagrama modular y de flujo | `docs/diagrama_modular.md`, `docs/diagramas/` |
| Capturas y explicaciones de Linux | `docs/evidencias/linux/` |
| Capturas y explicaciones del simulador | `docs/evidencias/simulador/` |
| Comparación simulación vs Linux | `docs/comparacion_simulacion_linux.md` |
| Revisión cruzada A → B | `docs/revision_cruzada_A_B.md` |
| Recorrido completo (T4.4) | `docs/validacion_t4.4.md` |
| Sesión de ejemplo | `pruebas/demo.txt` |
