# Contrato de Proceso y Planificadores

- **Tarea:** T1.2
- **Fase:** 1. Diseño
- **Responsable:** A
- **Depende de:** T0.3
- **Estado:** Contrato v1
- **Requisitos:** Python 3.10 o superior, solo biblioteca estándar.

Este documento define el contrato que deben respetar `procesos.py` y
`planificador.py`. Es la base para implementar la clase `Proceso`, los estados
y el resultado que devuelven FCFS, SJF y Round Robin.

## 1. Alcance

El contrato cubre:

1. Los campos y validaciones de `Proceso`.
2. Los estados del ciclo de vida y sus transiciones.
3. Las estructuras que devuelven los planificadores.
4. Las reglas comunes de planificación.
5. Un conjunto de datos verificados que sirve como prueba.

No incluye todavía la implementación de los módulos ni la interfaz de consola.

## 2. Modelo `Proceso`

### 2.1 Definición

```python
from dataclasses import dataclass
from enum import Enum


class EstadoProceso(str, Enum):
    NUEVO = "NUEVO"
    LISTO = "LISTO"
    EJECUTANDO = "EJECUTANDO"
    TERMINADO = "TERMINADO"
    RECHAZADO = "RECHAZADO"


@dataclass
class Proceso:
    pid: int
    nombre: str
    llegada: int
    cpu: int
    prioridad: int
    memoria: int
    estado: EstadoProceso = EstadoProceso.NUEVO
```

`Proceso` solo contiene los datos de entrada y su estado actual. Los tiempos
calculados por una planificación no se guardan dentro del proceso: viven en
`ResultadoPlanificacion`. Esto permite planificar varias veces con los mismos
procesos sin contaminar el estado.

### 2.2 Campos

| Campo | Tipo | Regla | Valor por defecto |
|---|---|---|---|
| `pid` | `int` | Entero único, empieza en 1 y nunca se reutiliza. | Lo asigna `procesos.py`. |
| `nombre` | `str` | Coincide con `^[A-Za-z_][A-Za-z0-9_]*$`; es único entre los procesos registrados y no puede ser palabra reservada. | Obligatorio. |
| `llegada` | `int` | Instante de llegada, `>= 0`. | `0` |
| `cpu` | `int` | Tiempo total de CPU requerido, `> 0`. | `1` |
| `prioridad` | `int` | `>= 0`; un número menor significa mayor prioridad, igual que `nice` en Linux. | `1` |
| `memoria` | `int` | Memoria requerida en MB, `> 0`. | `64` |
| `estado` | `EstadoProceso` | Uno de los cinco estados definidos. | `NUEVO` |

Los valores por defecto se aplican cuando el comando `crear proceso` omite el
atributo correspondiente. El parser entrega valores enteros ya convertidos; la
validación final la realiza `procesos.py`.

### 2.3 Validaciones

Antes de registrar un proceso se debe verificar:

1. `nombre` no está vacío, cumple la expresión regular y no es una palabra
   reservada de `tokens.py` (comparación sin distinguir mayúsculas).
2. No existe otro proceso registrado con el mismo `nombre`.
3. `llegada >= 0`.
4. `cpu > 0`.
5. `prioridad >= 0`.
6. `memoria > 0`.

Si una validación falla, `procesos.py` lanza `ValueError` con un mensaje claro.
El despachador lo captura y lo presenta al usuario como `[ERROR] ...`; nunca se
muestra un traceback.

### 2.4 Creación y memoria

El constructor de `Proceso` solo valida y almacena los campos; no reserva
memoria. La función de creación de `procesos.py` realiza esta secuencia:

1. Construye el proceso con estado `NUEVO`.
2. Solicita a `memoria.py` la cantidad indicada.
3. Si la memoria alcanza, cambia el estado a `LISTO` y registra el proceso.
4. Si no alcanza, cambia el estado a `RECHAZADO`, lo registra para que pueda
   consultarse y no le asigna memoria.

El `pid` se asigna en el momento de la creación, incluso si el proceso termina
en estado `RECHAZADO`. El `pid` no se reutiliza.

## 3. Estados

### 3.1 Significado

| Estado | Significado |
|---|---|
| `NUEVO` | El proceso fue construido, pero aún no se decidió si se admite. |
| `LISTO` | Fue admitido, tiene memoria reservada y espera CPU. |
| `EJECUTANDO` | Tiene la CPU asignada en una ejecución en vivo. |
| `TERMINADO` | Terminó su CPU o fue finalizado manualmente; su memoria fue liberada. |
| `RECHAZADO` | No fue admitido porque no había memoria suficiente. |

No se usa un estado `BLOQUEADO` porque el simulador no modela operaciones de
entrada/salida que bloqueen procesos.

### 3.2 Transiciones permitidas

| Desde | Hacia | Condición |
|---|---|---|
| `NUEVO` | `LISTO` | La memoria solicitada fue reservada. |
| `NUEVO` | `RECHAZADO` | No hay memoria suficiente. |
| `LISTO` | `EJECUTANDO` | El proceso recibe la CPU. |
| `EJECUTANDO` | `LISTO` | Round Robin lo interrumpe y aún le queda CPU. |
| `EJECUTANDO` | `TERMINADO` | Consume todo su tiempo de CPU. |
| `LISTO` o `EJECUTANDO` | `TERMINADO` | Se ejecuta `finalizar proceso`. |
| `TERMINADO` o `RECHAZADO` | Ninguno | Son estados finales. |

Al pasar a `TERMINADO` se libera la memoria del proceso. Un proceso
`RECHAZADO` nunca tuvo memoria reservada.

El comando `planificar` es una simulación: no cambia el estado ni la memoria de
los procesos. `EJECUTANDO` queda reservado para una ejecución en vivo o para
una extensión futura del simulador.

## 4. Contrato de los planificadores

### 4.1 Estructuras de retorno

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Ejecucion:
    pid: int
    nombre: str
    inicio: int
    fin: int


@dataclass(frozen=True)
class TiempoProceso:
    pid: int
    nombre: str
    llegada: int
    cpu: int
    inicio: int
    fin: int
    retorno: int
    espera: int


@dataclass(frozen=True)
class ResultadoPlanificacion:
    algoritmo: str
    quantum: int | None
    ejecuciones: list[Ejecucion]
    tiempos: list[TiempoProceso]
    promedio_retorno: float
    promedio_espera: float
```

Significado:

- `Ejecucion` es un segmento continuo de CPU. El Gantt completo es la lista
  ordenada de estos segmentos.
- `TiempoProceso` contiene los tiempos calculados de un proceso.
- `ResultadoPlanificacion` agrupa el Gantt, los tiempos y los promedios.
- `algoritmo` toma los valores `"FCFS"`, `"SJF"` o `"RR"`.
- `quantum` es `None` para FCFS y SJF; para RR es el quantum utilizado.
- `tiempos` se ordena por `pid` ascendente.
- Los promedios son `float`; la consola los muestra con dos decimales.

### 4.2 Firmas

```python
def fcfs(procesos: list[Proceso]) -> ResultadoPlanificacion:
    ...


def sjf(procesos: list[Proceso]) -> ResultadoPlanificacion:
    ...


def rr(procesos: list[Proceso], quantum: int = 3) -> ResultadoPlanificacion:
    ...
```

### 4.3 Reglas comunes

1. Los planificadores no modifican los objetos `Proceso` recibidos. Simulan con
   copias locales del tiempo restante y pueden ejecutarse varias veces con el
   mismo resultado.
2. Solo se consideran procesos en estado `LISTO`. Los procesos `NUEVO`,
   `EJECUTANDO`, `TERMINADO` y `RECHAZADO` se ignoran.
3. La prioridad no se usa en FCFS, SJF ni Round Robin; solo se conserva como
   dato del proceso.
4. La memoria no afecta el orden de planificación.
5. Si no hay procesos `LISTO`, se retorna un resultado con listas vacías y
   promedios `0.0`.
6. Si la CPU queda libre y no hay procesos listos, el tiempo avanza hasta la
   siguiente llegada. Ese intervalo no genera una `Ejecucion`; al imprimir el
   Gantt se muestra como `(libre)`.
7. Los empates se resuelven por `pid` ascendente, salvo que una regla indique
   otra cosa.
8. El tiempo es discreto y se mide en unidades enteras no negativas.

### 4.4 FCFS

- Ordena los procesos por `(llegada, pid)`.
- Ejecuta cada proceso completo, sin expropiación.
- `inicio` es el mayor valor entre el tiempo actual y la llegada del proceso.
- `fin = inicio + cpu`.
- No hay quantum.

### 4.5 SJF no expulsivo

- Al quedar libre la CPU, elige entre los procesos que ya llegaron y no han
  terminado el de menor `(cpu, llegada, pid)`.
- Ejecuta el proceso elegido completo, sin expropiación.
- Si no hay procesos disponibles, avanza hasta la siguiente llegada.
- No hay quantum.

### 4.6 Round Robin

- Usa una cola FIFO con `collections.deque`.
- `quantum` debe ser un entero `>= 1`; si no, se lanza `ValueError`.
- Al iniciar, se encolan los procesos con `llegada == 0`, ordenados por `pid`.
  Las demás llegadas se incorporan cuando ocurren.
- Si la CPU está libre, avanza hasta la siguiente llegada y encola todos los
  procesos de ese instante ordenados por `pid`.
- Cada proceso ejecuta como máximo `quantum` unidades o hasta terminar.
- Al final de un quantum, primero se encolan las llegadas de ese instante y
  después se reencola el proceso interrumpido, si aún le queda CPU. Por eso un
  proceso que llega justo cuando termina un quantum entra antes que el proceso
  interrumpido.
- Si al proceso le queda menos o igual que el quantum, termina en ese segmento.
- Un mismo `pid` puede aparecer varias veces en `ejecuciones`.

### 4.7 Cálculo de tiempos

Para cada proceso planificado:

```text
retorno = fin - llegada
espera  = retorno - cpu
```

`inicio` es el instante del primer segmento de CPU del proceso. `fin` es el
instante en que termina por completo.

Los promedios se calculan solo sobre los procesos incluidos en `tiempos`:

```text
promedio_retorno = suma(retorno) / cantidad
promedio_espera  = suma(espera)  / cantidad
```

Si `cantidad == 0`, ambos promedios son `0.0`. No se redondean dentro del
planificador; el formateo a dos decimales corresponde a la consola.

### 4.8 Representación del Gantt

`ejecuciones` contiene solo intervalos en los que un proceso usa la CPU, en
orden cronológico. No se agregan bloques artificiales para la CPU libre. El
despachador, al imprimir, rellena los huecos entre segmentos con `(libre)`.

Ejemplo de formato de salida:

```text
Gantt FCFS:
[0-8] P1   [8-12] P2   [12-21] P3   [21-26] P4
```

## 5. Datos verificados

Estos son los datos que debe cargar el comando `ejemplo`:

| Proceso | Llegada | CPU | Prioridad | Memoria (MB) |
|---|---:|---:|---:|---:|
| P1 | 0 | 8 | 2 | 128 |
| P2 | 1 | 4 | 1 | 64 |
| P3 | 2 | 9 | 3 | 256 |
| P4 | 3 | 5 | 2 | 100 |

Los cuatro procesos quedan en estado `LISTO` y consumen 548 MB de memoria.

### 5.1 FCFS

Gantt:

```text
P1 0-8, P2 8-12, P3 12-21, P4 21-26
```

| Proceso | Inicio | Fin | Retorno | Espera |
|---|---:|---:|---:|---:|
| P1 | 0 | 8 | 8 | 0 |
| P2 | 8 | 12 | 11 | 7 |
| P3 | 12 | 21 | 19 | 10 |
| P4 | 21 | 26 | 23 | 18 |

Promedios: retorno `15.25`, espera `8.75`.

### 5.2 SJF no expulsivo

Gantt:

```text
P1 0-8, P2 8-12, P4 12-17, P3 17-26
```

| Proceso | Inicio | Fin | Retorno | Espera |
|---|---:|---:|---:|---:|
| P1 | 0 | 8 | 8 | 0 |
| P2 | 8 | 12 | 11 | 7 |
| P3 | 17 | 26 | 24 | 15 |
| P4 | 12 | 17 | 14 | 9 |

Promedios: retorno `14.25`, espera `7.75`.

### 5.3 Round Robin con quantum 3

Gantt:

```text
P1 0-3, P2 3-6, P3 6-9, P4 9-12, P1 12-15, P2 15-16,
P3 16-19, P4 19-21, P1 21-23, P3 23-26
```

| Proceso | Inicio | Fin | Retorno | Espera |
|---|---:|---:|---:|---:|
| P1 | 0 | 23 | 23 | 15 |
| P2 | 3 | 16 | 15 | 11 |
| P3 | 6 | 26 | 24 | 15 |
| P4 | 9 | 21 | 18 | 13 |

Promedios: retorno `20.00`, espera `13.50`.

### 5.4 Resumen

| Comando | Finalización (P1, P2, P3, P4) | Retorno promedio | Espera promedio |
|---|---|---:|---:|
| `planificar fcfs` | 8, 12, 21, 26 | 15.25 | 8.75 |
| `planificar sjf` | 8, 12, 26, 17 | 14.25 | 7.75 |
| `planificar rr quantum=3` | 23, 16, 26, 21 | 20.00 | 13.50 |

## 6. Errores y convenciones

- Los errores de validación del proceso se lanzan como `ValueError`.
- Los errores de quantum se lanzan como `ValueError`.
- Los mensajes al usuario empiezan con `[ERROR]` y explican la causa.
- Los mensajes exitosos empiezan con `[OK]`.
- No se usan dependencias externas; solo `dataclasses`, `enum`,
  `collections.deque` y demás biblioteca estándar.
- Los nombres internos usan español y `snake_case`; los comandos se escriben en
  minúsculas y sin tildes.

## 7. Criterios de aceptación de T1.2

- [x] Campos de `Proceso` definidos con tipo, regla y valor por defecto.
- [x] Estados y transiciones definidos.
- [x] Estructuras de retorno de los planificadores definidas.
- [x] Reglas de FCFS, SJF y Round Robin definidas.
- [x] Fórmulas de retorno y espera definidas.
- [x] Ejemplo con los cuatro procesos y los tres algoritmos verificado.
- [x] Contrato compatible con Python 3.10+ y biblioteca estándar.
