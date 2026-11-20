# Guia de practicas de Linux

- **Tarea:** T3.12 (alimenta T6.3)
- **Responsable:** D
- **Que se pide:** practicas de **procesos, prioridades, hilos y permisos**, cada una con
  captura y 2 o 3 lineas de explicacion.

## Como trabajar

1. Abre una terminal normal. No hace falta ser root ni instalar nada.
2. Para cada practica: ejecuta los comandos en orden, toma la captura cuando diga
   **[CAPTURA]**, y escribe la explicacion en la plantilla del final.
3. Guarda las capturas como `docs/evidencias/linux/NN_descripcion.png`
   (por ejemplo `01_ps_aux.png`). La carpeta se crea con:

```bash
mkdir -p docs/evidencias/linux
```

4. En cada captura debe verse el comando escrito y su salida. Si es muy larga, recorta
   con `| head -15`.
5. Al terminar, todos los procesos de prueba deben quedar cerrados (ver Limpieza).

---

## Practica 1. Procesos

**Objetivo:** ver que procesos existen, su PID, su estado y como se relacionan (padre e hijo).
Equivale en el simulador a `listar procesos`, `consultar proceso` y `finalizar proceso`.

```bash
# Lanzar un proceso de prueba en segundo plano
sleep 300 &
```

```bash
# 1.1 Lista de procesos (PID, usuario, estado, comando)
ps aux | head -15
```

**[CAPTURA 01]** `01_ps_aux.png`

```bash
# 1.2 Consultar un proceso concreto por su PID ($! es el PID del ultimo "&")
ps -o pid,ppid,stat,ni,cmd -p $!
```

**[CAPTURA 02]** `02_ps_pid.png`

```bash
# 1.3 Arbol de procesos: quien es padre de quien
pstree -p | head -20
```

**[CAPTURA 03]** `03_pstree.png`

```bash
# 1.4 Finalizar el proceso
kill $!
ps -p $! || echo "El proceso ya no existe"
```

**[CAPTURA 04]** `04_kill.png`

**Que observar**
- `PID`: identificador unico. `PPID`: PID del proceso padre.
- `STAT`: `S` dormido, `R` ejecutando o listo, `Z` zombie, `T` detenido.
- Todo proceso tiene un padre; el arbol nace en `systemd` (PID 1).
- `top` (tecla `q` para salir) muestra los procesos en vivo, con uso de CPU y memoria.

**Idea para la explicacion:** el SO guarda para cada proceso un PID, su estado y su padre,
igual que la clase `Proceso` del simulador (pid, nombre, estado). La diferencia es que
Linux tambien registra al padre y mucha mas informacion.

---

## Practica 2. Prioridades

**Objetivo:** cambiar la prioridad de un proceso con `nice`. Equivale al campo `prioridad`
del simulador.

```bash
# 2.1 Lanzar un proceso con prioridad normal y otro con "nice" 10 (menos prioridad)
sleep 300 &
nice -n 10 sleep 300 &
```

```bash
# 2.2 Comparar la columna NI (valor nice) y PRI (prioridad)
ps -o pid,ni,pri,stat,cmd -C sleep
```

**[CAPTURA 05]** `05_nice.png`

```bash
# 2.3 Cambiar la prioridad de uno que ya corre (reemplaza PID por el real)
renice -n 15 -p PID
ps -o pid,ni,pri,cmd -p PID
```

**[CAPTURA 06]** `06_renice.png`

```bash
# 2.4 Verlo en vivo: en top, mira la columna NI
top -b -n 1 | head -15
```

**[CAPTURA 07]** `07_top_ni.png` (opcional)

**Que observar**
- El nice del proceso normal suele ser 0, pero depende de la terminal: si el tuyo muestra otro
  valor base (por ejemplo 5), lo importante es que el segundo proceso tenga **10 mas** que el
  primero.
- El valor **nice** va de -20 (mas prioridad) a 19 (menos prioridad). Por defecto es 0.
- Un usuario normal solo puede **subir** el nice (bajar prioridad). Bajarlo por debajo de 0
  requiere `sudo`. No lo hagas; basta con mostrar el limite:

```bash
renice -n -5 -p PID
```

  Debe responder `Permission denied` (o similar). **[CAPTURA 08]** `08_renice_denegado.png`
- Un nice mas alto no detiene al proceso: solo le da menos turnos de CPU cuando hay competencia.

**Idea para la explicacion:** Linux usa la prioridad para decidir que proceso recibe CPU
primero; el simulador usa `prioridad` como dato del proceso, pero sus algoritmos (FCFS, SJF y
RR) deciden por llegada, duracion o turno, no por prioridad.

---

## Practica 3. Hilos

**Objetivo:** ver que un proceso puede tener varios hilos que comparten memoria. Equivale a
`hilos_sync.py` (concurrencia).

```bash
# 3.1 Procesos con mas de un hilo (NLWP = numero de hilos)
ps -eo pid,nlwp,comm --sort=-nlwp | head -10
```

**[CAPTURA 09]** `09_nlwp.png`

```bash
# 3.2 Hilos de un proceso concreto (elige un PID con varios hilos, p. ej. el primero de arriba)
ps -L -o pid,lwp,nlwp,stat,comm -p PID | head -15
```

**[CAPTURA 10]** `10_hilos_proceso.png`

```bash
# 3.3 Vista de hilos en vivo
top -H -b -n 1 | head -15
```

**[CAPTURA 11]** `11_top_hilos.png`

```bash
# 3.4 Un programa con hilos propios: nuestro simulador
python3 -c "
import threading, time
hilos = [threading.Thread(target=time.sleep, args=(20,)) for _ in range(4)]
[h.start() for h in hilos]
import os; os.system('ps -L -o pid,lwp,nlwp,comm -p %d' % os.getpid())
"
```

**[CAPTURA 12]** `12_python_hilos.png`

**Que observar**
- `PID` es el mismo para todos los hilos del proceso; `LWP` es el id de cada hilo.
- `NLWP` cuenta cuantos hilos tiene el proceso (Python con 4 hilos mostrara 5: el principal
  mas 4).
- Los hilos comparten la memoria del proceso; por eso necesitan Lock o Semaphore
  (ver `hilos_sync.py`).

**Idea para la explicacion:** un hilo es un flujo de ejecucion dentro de un proceso. En el
simulador, `concurrencia sin_lock` muestra el problema de compartir un contador sin proteger
y `con_lock`/`semaforo` lo resuelven; en Linux ocurre lo mismo cuando varios hilos tocan los
mismos datos.

Para la demo del simulador junto a esta practica (cuando `consola.py` este integrado):

```bash
python3 main.py --script pruebas/demo.txt
```

Mientras tanto se puede usar directamente:

```bash
python3 -c "import hilos_sync as h; [print(h.formatear_resultado(h.ejecutar_concurrencia(m))) for m in h.MODOS]"
```

**[CAPTURA 13]** `13_simulador_hilos.png` (esta es para la tabla de T6.3)

---

## Practica 4. Permisos

**Objetivo:** ver y cambiar quien puede leer, escribir o ejecutar un archivo. Se relaciona con
`archivos.py` (el simulador solo trabaja dentro de `carpeta_pruebas/`).

```bash
# 4.1 Preparar una carpeta de prueba
mkdir -p ~/practica_permisos && cd ~/practica_permisos
echo "contenido de prueba" > nota.txt
ls -l nota.txt
```

**[CAPTURA 14]** `14_ls_l.png`

```bash
# 4.2 Quitar permiso de lectura y comprobar que falla
chmod 200 nota.txt
ls -l nota.txt
cat nota.txt
```

**[CAPTURA 15]** `15_sin_lectura.png` (debe verse `Permission denied`)

```bash
# 4.3 Restaurar y dar permiso de ejecucion a un script
chmod 644 nota.txt
printf '#!/bin/sh\necho hola desde el script\n' > hola.sh
./hola.sh                 # falla: sin permiso de ejecucion
chmod 755 hola.sh
./hola.sh                 # ahora funciona
ls -l hola.sh
```

**[CAPTURA 16]** `16_chmod_ejecucion.png`

```bash
# 4.4 Permisos simbolicos y duenio
chmod u+x,g-w,o-r nota.txt
ls -l nota.txt
id
```

**[CAPTURA 17]** `17_chmod_simbolico.png`

**Que observar**
- `-rwxr-xr--` se lee en tres bloques: **usuario**, **grupo**, **otros**. Cada uno con `r` (leer),
  `w` (escribir) y `x` (ejecutar).
- En numeros: `r=4`, `w=2`, `x=1`. Asi `644` = `rw-r--r--` y `755` = `rwxr-xr-x`.
- Un archivo sin `x` no se puede ejecutar aunque sea un script valido.

**Idea para la explicacion:** Linux controla el acceso por usuario, grupo y otros. El simulador
no tiene usuarios; su proteccion consiste en confinar las operaciones a `carpeta_pruebas/` y
rechazar rutas con `..`.

---

## Limpieza

```bash
pkill -u "$USER" sleep      # cierra los "sleep" de prueba (solo los tuyos)
cd ~ && rm -r ~/practica_permisos
jobs                        # no debe quedar nada en segundo plano
```

---

## Plantilla de evidencias (para copiar al informe)

Para cada practica, una captura y 2 o 3 lineas. Ejemplo ya redactado de la estructura:

| N.º | Practica | Comando | Captura | Explicacion (2 o 3 lineas) |
|---|---|---|---|---|
| 1 | Procesos | `ps aux`, `pstree -p` | `01_ps_aux.png` | _Escribir aqui lo observado: PID, PPID, estado._ |
| 2 | Prioridades | `nice`, `renice`, `ps -o ni` | `05_nice.png` | _Escribir aqui lo observado: efecto del valor nice y limite sin sudo._ |
| 3 | Hilos | `ps -L`, `top -H` | `10_hilos_proceso.png` | _Escribir aqui lo observado: mismo PID, distintos LWP._ |
| 4 | Permisos | `ls -l`, `chmod` | `15_sin_lectura.png` | _Escribir aqui lo observado: lectura denegada tras chmod._ |

## Tabla de comparacion simulacion vs Linux (borrador para T6.3)

La columna de Linux se llena con lo que observes aqui; la del simulador se completa cuando
`consola.py` este integrado (T5.4).

| Aspecto | Simulador (Python) | Linux real | Que observe |
|---|---|---|---|
| Proceso | Clase `Proceso` con pid, nombre, llegada, cpu, prioridad, memoria, estado | PID, PPID, estado, usuario, memoria, etc. | _completar_ |
| Planificacion | FCFS, SJF no expulsivo y RR, decididos por llegada, duracion o turno | Planificador del nucleo con prioridades dinamicas | _completar_ |
| Prioridad | Dato del proceso; no la usan los algoritmos | `nice` de -20 a 19, afecta el reparto de CPU | _completar_ |
| Hilos | 4 hilos sobre un contador; `sin_lock`, `con_lock`, `semaforo` | Hilos del proceso (LWP) que comparten memoria | _completar_ |
| Sincronizacion | `threading.Lock` y `Semaphore(1)` | Mutex y semaforos del sistema | _completar_ |
| Memoria | Tope fijo de 1024 MB, reservar y liberar | Memoria virtual, paginacion, RAM del equipo | _completar_ |
| Archivos | Solo dentro de `carpeta_pruebas/` | Todo el sistema de archivos con permisos | _completar_ |
| Permisos | No hay usuarios; se confina a una carpeta | rwx por usuario, grupo y otros | _completar_ |
