# Evidencias Linux y comparación con el simulador (T6.3)

Este documento reúne las evidencias de las prácticas en Linux (T3.12) y de la ejecución del
simulador (T5.4), y las compara. Las capturas están en:

- Linux: `docs/evidencias/linux/` (explicaciones en `explicaciones.md`)
- Simulador: `docs/evidencias/simulador/` (explicaciones en `explicaciones.md`)

## 1. Resumen de evidencias

| Tema | Captura Linux | Captura simulador |
|---|---|---|
| Procesos | `01_ps_aux.png`, `02_ps_pid.png`, `03_pstree.png`, `04_kill.png` | `02_procesos.png`, `06_memoria.png` (finalizar proceso) |
| Prioridades | `05_nice.png`, `06_renice.png`, `08_renice_denegado.png` | `02_procesos.png` (columna Prioridad) |
| Planificación | — (la hace el núcleo de Linux) | `03_fcfs.png`, `04_sjf.png`, `05_round_robin.png` |
| Hilos y sincronización | `09_nlwp.png`, `10_hilos_proceso.png`, `11_top_hilos.png`, `12_python_hilos.png` | `07_concurrencia.png` |
| Memoria | `11_top_hilos.png` (columnas VIRT, RES) | `06_memoria.png` |
| Archivos y permisos | `14_ls_l.png`, `15_sin_lectura.png`, `16_chmod_ejecucion.png`, `17_chmod_simbolico.png` | `08_mensajes_archivos.png`, `09_errores.png` |
| Hilos con el simulador en Linux | `13_simulador_hilos.png` | `07_concurrencia.png` |

## 2. Tabla de comparación: simulación vs Linux

| Aspecto | Simulador (Python) | Linux real | Qué se observó |
|---|---|---|---|
| **Proceso** | Clase `Proceso` con pid, nombre, llegada, CPU, prioridad, memoria y estado (`NUEVO`, `LISTO`, `EJECUTANDO`, `TERMINADO`, `RECHAZADO`). Los pid son consecutivos (1 a 4). | PID único, PPID (proceso padre), usuario, estado (`S`, `R`, `Z`, `T`...), memoria y muchos más datos. Forma un árbol que nace en `systemd` (PID 1). | En Linux cada proceso tiene un padre (`PPID`); en el simulador no existe esa relación. Ambos identifican al proceso con un número único. |
| **Crear y finalizar** | `crear proceso`, `finalizar proceso <pid>`; finalizar libera la memoria. | Se lanza con `sleep 600 &` y se termina con `kill <pid>`. | Ambos terminan el proceso por su identificador. En Linux `kill` envía una señal y el sistema confirma `terminated`; en el simulador responde `[OK] ... finalizado`. |
| **Planificación** | FCFS, SJF no expulsivo y Round Robin sobre un conjunto fijo de procesos. Se muestra un diagrama de Gantt y los promedios (FCFS 15,25 / 8,75; SJF 14,25 / 7,75; RR 20,00 / 13,50 de retorno / espera). | El núcleo reparte la CPU de forma continua entre cientos de procesos con prioridades dinámicas; no se elige un algoritmo desde la terminal. | El simulador permite comparar algoritmos de forma aislada y ver sus resultados; en Linux solo se observa el resultado (por ejemplo, el uso de CPU en `top`). |
| **Prioridad** | Campo `prioridad` en cada proceso, pero FCFS, SJF y RR **no la usan** para decidir. | Valor `nice` de -20 a 19. Con `renice -n 19` el proceso pasó de `NI 5` a `NI 19` y su `PRI` bajó de 14 a 0. Subir la prioridad (`renice -n -5`) dio "Permiso denegado" sin `sudo`. | En Linux la prioridad sí cambia el reparto de CPU y tiene control de permisos; en el simulador es solo un dato informativo. |
| **Hilos** | `hilos_sync.py` crea 4 hilos con `threading` que incrementan un contador compartido. | Un proceso puede tener muchos hilos: `NLWP` 63 en un proceso de escritorio. Un programa Python con 4 hilos aparece con `NLWP` 5 (4 más el principal). | Ambos usan hilos reales del sistema. En Linux todos comparten el mismo PID y se distinguen por `LWP`, y `top -H` mostró que comparten la misma memoria (`VIRT`, `RES`). |
| **Sincronización** | `sin_lock`: 1000 de 4000 (se pierden 3000 incrementos, condición de carrera). `con_lock` y `semaforo`: 4000 de 4000. | El mismo programa Python se ejecuta sobre hilos del sistema (captura 13). Los hilos comparten la memoria del proceso, por eso necesitan mecanismos de exclusión. | La condición de carrera es real: ocurre porque los hilos comparten datos. `Lock` y `Semaphore(1)` la evitan al dejar entrar a un solo hilo a la sección crítica. |
| **Memoria** | Tope fijo de 1024 MB. Reservar al crear y liberar al finalizar. Con 548 MB usados, pedir 2000 MB da `[ERROR]`; tras finalizar P1 quedan 420 MB usados y 604 libres. | Memoria virtual: cada proceso tiene `VIRT` (dirección virtual reservada) y `RES` (memoria física en uso); el total depende de la RAM del equipo (15605 MiB). | El simulador modela la capacidad como un número que se resta y se devuelve; Linux distingue memoria virtual de física y puede reservar más de lo que hay. |
| **Archivos** | CRUD solo dentro de `carpeta_pruebas/`. Rechaza rutas con `..`, rutas absolutas y enlaces (la prueba `archivo leer ../secreto.txt` fue rechazada sin errores técnicos). | Todo el sistema de archivos, con permisos por usuario, grupo y otros. | El simulador protege con una carpeta confinada; Linux protege con permisos aplicados a cada archivo. |
| **Permisos** | No hay usuarios ni permisos. | `-rw-rw-r--` por defecto; con `chmod 200` ni el dueño pudo leer el archivo ("Permiso denegado"); un script sin `x` no se ejecutó hasta `chmod 755`; `chmod u+x,g-w,o-r` dejó `rwxr-----`. | Linux decide el acceso por usuario, grupo y otros (`id` mostró los grupos del usuario); el simulador solo valida la ruta. |
| **Comunicación** | Cola FIFO: `mensaje enviar` y `mensaje recibir` (`hola` sale primero que lo que se envíe después). | Existen mecanismos reales (tuberías, colas de mensajes del sistema); no se practicaron en este proyecto. | Solo se evidenció el simulador; la comparación se deja como limitación. |
| **Manejo de errores** | Mensajes `[OK]` y `[ERROR]` con explicación y el uso correcto; nunca se muestra un traceback. | Mensajes del sistema (`Permiso denegado`, `no existe el proceso`), a veces en inglés o con usos largos. | Ambos informan el motivo del fallo; el simulador lo hace de forma más guiada. |

## 3. Conclusiones de la comparación

1. **Qué modela bien el simulador:** el ciclo de vida de un proceso, el efecto de cada algoritmo
   de planificación sobre los promedios de espera y retorno, la reserva y liberación de memoria,
   y la condición de carrera con su solución (Lock y Semaphore). Son versiones reducidas y
   controladas de lo que hace un sistema operativo.
2. **Qué simplifica:** no existe el proceso padre, la prioridad no influye en la planificación,
   la memoria es solo un tope, y no hay usuarios ni permisos.
3. **Qué aporta Linux real:** escala (cientos de procesos y hilos al mismo tiempo), control de
   acceso por usuario y grupo, memoria virtual y una prioridad que sí cambia el reparto de CPU.
4. **Relación entre ambos:** `hilos_sync.py` se ejecutó dentro de Linux (captura 13) y usa el
   módulo `threading` de Python. Un programa Python con hilos aparece en Linux como hilos del
   sistema (`ps -L`, captura 12), lo que indica que los hilos del simulador son hilos reales
   y no solo una imitación.
