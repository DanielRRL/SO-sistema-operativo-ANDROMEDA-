# Firmas y Stubs de los Modulos

- **Tarea:** T1.3
- **Fase:** 1. Diseno
- **Responsables:** A, B, C, D
- **Depende de:** T1.1, T1.2
- **Estado:** v1
- **Requisitos:** Python 3.10 o superior, solo biblioteca estandar.

Este documento fija las firmas publicas de cada modulo y el comportamiento
temporal de sus stubs. Todos los stubs deben poder importarse sin errores y
deben devolver datos falsos seguros mientras se implementan las tareas de las
fases 3 y 4.

## 1. Decisiones de diseno

- Las firmas usan type hints compatibles con Python 3.10.
- Los stubs no realizan operaciones reales de archivos, memoria, hilos ni
  planificacion.
- Los stubs devuelven estructuras vacias o datos falsos; no lanzan
  `NotImplementedError` para no romper la consola ni las pruebas de humo.
- Se lanzan `ValueError` solo en validaciones simples que ya forman parte del
  contrato, como un quantum menor que 1 o un modo de concurrencia desconocido.
- `main.py` ya esta implementado y no se modifica en T1.3.
- `lexer.tokenizar` mantiene un tokenizador falso por espacios para que
  `python3 main.py` siga funcionando mientras B implementa el lexer real.

### 1.1 Sintaxis de referencia

La sintaxis de integracion se toma del plan original y del contrato T1.2:

```text
crear proceso <nombre> llegada=<n> cpu=<n> prioridad=<n> mem=<n>
listar procesos
consultar proceso <pid>
finalizar proceso <pid>
planificar rr quantum=<n>
concurrencia sin_lock|con_lock|semaforo
memoria estado
memoria asignar <pid> <mb>
memoria liberar <pid>
```

El documento T1.1 propone una version mas corta y posicional:

```text
crear <nombre> <llegada> <cpu> <prioridad> <memoria>
listar
hilos sin_lock|con_lock|semaforo
memoria
```

T1.1 queda como propuesta de simplificacion. Antes de implementar `tokens.py`,
`lexer.py` y `parser.py` en T2.3/T3.5/T3.9, el equipo debe alinearla con la
sintaxis de referencia. Las firmas de T1.3 son independientes de esa decision.

## 2. Mapa de dependencias

```text
tokens.py
   |
   v
lexer.py ---> parser.py ---> consola.py
                               |
                               +--> procesos.py ---> memoria.py
                               +--> planificador.py ---> procesos.py
                               +--> estadisticas.py ---> planificador.py
                               +--> archivos.py
                               +--> hilos_sync.py
                               +--> mensajes.py

main.py ---> lexer.py (integracion temporal de T2.1)
```

## 3. `tokens.py`

Responsable: B.

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `DefinicionToken` | `@dataclass(frozen=True)` con `palabra`, `tipo`, `definicion`, `ejemplo`, `sintaxis` | Fila de la tabla de terminales. |
| `PALABRAS` | `tuple[str, ...]` | Palabras reservadas del lenguaje. |
| `RESERVADAS` | `dict[str, str]` | Mapa palabra en minusculas -> tipo de token. |
| `TERMINALES` | `dict[str, DefinicionToken]` | Tabla completa usada por `ayuda` y el lexer. |
| `buscar_definicion` | `buscar_definicion(palabra: str) -> DefinicionToken \| None` | Definicion de una palabra, o `None`. |
| `listar_definiciones` | `listar_definiciones() -> list[DefinicionToken]` | Todas las definiciones registradas. |

Stub T1.3: las constantes quedan vacias y las funciones devuelven `None` o una
lista vacia. La tabla completa se carga en T2.3.

## 4. `lexer.py`

Responsable: B.

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `Token` | `@dataclass(frozen=True)` con `tipo`, `lexema`, `columna` | Token reconocido por el lexer. |
| `tokenizar` | `tokenizar(linea: str) -> list[Token]` | Lista de tokens, siempre terminada en `FIN`. |

Stub T1.3: separa por espacios, consulta `RESERVADAS` si ya tiene datos y
genera tokens `PALABRA` o el tipo reservado correspondiente. Si no hay palabras
reservadas cargadas, todos los lexemas no vacios son `PALABRA`. Agrega
`Token("FIN", "", len(linea) + 1)`.

La implementacion real con expresiones regulares, cadenas, nombres de archivo,
numeros y errores con columna corresponde a T3.5.

## 5. `parser.py`

Responsable: C.

```python
@dataclass(frozen=True)
class Orden:
    comando: str
    subcomando: str | None = None
    argumentos: tuple[str | int, ...] = ()
    atributos: dict[str, int] = field(default_factory=dict)
    linea_original: str = ""
```

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `Orden` | Dataclass anterior | Orden estructurada que recibe el despachador. |
| `parsear` | `parsear(tokens: list[Token]) -> Orden` | Orden validada; lanza `ValueError` si la gramatica no es correcta. |

Stub T1.3: usa el primer token como `comando`, el resto como `argumentos` y
junta los lexemas en `linea_original`. No valida la gramatica todavia. La
validacion completa corresponde a T3.9.

## 6. `consola.py`

Responsable: C.

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `despachar` | `despachar(orden: Orden) -> str` | Ejecuta la orden y devuelve el texto para imprimir. |
| `ayuda` | `ayuda(palabra: str \| None = None) -> str` | Ayuda general o detalle de una palabra. |

Stub T1.3: `despachar` devuelve `[ERROR] Despacho pendiente...` y `ayuda`
devuelve un mensaje de ayuda pendiente. La conexion real con los modulos
corresponde a T4.1.

## 7. `procesos.py`

Responsable: A.

```python
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

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `crear_proceso` | `crear_proceso(nombre: str, llegada: int = 0, cpu: int = 1, prioridad: int = 1, memoria: int = 64) -> Proceso` | Proceso creado. |
| `listar_procesos` | `listar_procesos() -> list[Proceso]` | Procesos registrados. |
| `consultar_proceso` | `consultar_proceso(pid: int) -> Proceso \| None` | Proceso con ese pid, o `None`. |
| `finalizar_proceso` | `finalizar_proceso(pid: int) -> Proceso \| None` | Proceso finalizado, o `None` si no existe. |
| `cargar_ejemplo` | `cargar_ejemplo() -> list[Proceso]` | Los cuatro procesos verificados P1-P4 en estado `LISTO`. |

Stub T1.3: `crear_proceso` devuelve un proceso falso con `pid=0` y estado
`LISTO`; `listar_procesos` devuelve `[]`; las consultas y finalizaciones
devuelven `None`; `cargar_ejemplo` devuelve los datos P1-P4 del contrato.

La validacion real, el registro, la asignacion de pid y la integracion con
memoria corresponden a T3.1 y T4.2.

## 8. `planificador.py`

Responsable: A.

```python
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

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `fcfs` | `fcfs(procesos: list[Proceso]) -> ResultadoPlanificacion` | Resultado FCFS. |
| `sjf` | `sjf(procesos: list[Proceso]) -> ResultadoPlanificacion` | Resultado SJF no expulsivo. |
| `rr` | `rr(procesos: list[Proceso], quantum: int = 3) -> ResultadoPlanificacion` | Resultado Round Robin. |
| `planificar` | `planificar(procesos: list[Proceso], algoritmo: str, quantum: int = 3) -> ResultadoPlanificacion` | Despacha al algoritmo indicado. |

Stub T1.3: los tres planificadores devuelven un `ResultadoPlanificacion` vacio
con listas vacias y promedios `0.0`. `rr` valida que `quantum >= 1` y
`planificar` acepta `FCFS`, `SJF` y `RR` sin distinguir mayusculas.

La implementacion real debe respetar `docs/contrato_proceso.md` y
`docs/pseudocodigo_planificadores.md`.

## 9. `estadisticas.py`

Responsable: A.

```python
@dataclass(frozen=True)
class Estadisticas:
    algoritmo: str
    tiempos: list[TiempoProceso]
    promedio_retorno: float
    promedio_espera: float
```

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `calcular_estadisticas` | `calcular_estadisticas(resultado: ResultadoPlanificacion) -> Estadisticas` | Tiempos y promedios de una planificacion. |
| `formatear_estadisticas` | `formatear_estadisticas(estadisticas: Estadisticas) -> str` | Tabla de texto para la consola. |

Stub T1.3: devuelve estadisticas vacias y un mensaje temporal. La tabla real se
implementa en T3.4.

## 10. `memoria.py`

Responsable: B.

```python
CAPACIDAD_TOTAL = 1024


@dataclass(frozen=True)
class EstadoMemoria:
    total: int
    usada: int
    libre: int
    asignaciones: dict[int, int] = field(default_factory=dict)
```

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `reservar` | `reservar(pid: int, cantidad: int) -> bool` | `True` si se reservo, `False` si no hay espacio. |
| `liberar` | `liberar(pid: int) -> int` | MB liberados; `0` si el pid no tenia memoria. |
| `estado_memoria` | `estado_memoria() -> EstadoMemoria` | Total, usada, libre y asignaciones. |
| `reiniciar_memoria` | `reiniciar_memoria() -> None` | Deja la memoria como al inicio. |

Stub T1.3: `reservar` devuelve `True`, `liberar` devuelve `0` y
`estado_memoria` devuelve 1024 MB libres sin asignaciones. La validacion real de
capacidad corresponde a T3.7.

## 11. `archivos.py`

Responsable: B.

```python
CARPETA_PRUEBAS = Path("carpeta_pruebas")


@dataclass(frozen=True)
class ArchivoInfo:
    nombre: str
    tamano: int
```

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `validar_nombre` | `validar_nombre(nombre: str) -> str` | Nombre validado; lanza `ValueError` si es inseguro. |
| `crear_archivo` | `crear_archivo(nombre: str, contenido: str = "") -> ArchivoInfo` | Archivo creado. |
| `listar_archivos` | `listar_archivos() -> list[ArchivoInfo]` | Archivos de `carpeta_pruebas`. |
| `leer_archivo` | `leer_archivo(nombre: str) -> str` | Contenido del archivo. |
| `modificar_archivo` | `modificar_archivo(nombre: str, contenido: str) -> ArchivoInfo` | Archivo modificado; agrega texto al final. |
| `eliminar_archivo` | `eliminar_archivo(nombre: str) -> bool` | `True` si se elimino. |
| `existe_archivo` | `existe_archivo(nombre: str) -> bool` | `True` si existe dentro de la carpeta de pruebas. |

Stub T1.3: ninguna funcion toca el disco. `crear_archivo` y
`modificar_archivo` devuelven `ArchivoInfo` falso; `listar_archivos` devuelve
`[]`; `leer_archivo` devuelve `""`; `eliminar_archivo` devuelve `True`;
`existe_archivo` devuelve `False`; `validar_nombre` devuelve el nombre sin
validar todavia. La seguridad de rutas corresponde a T3.8.

## 12. `hilos_sync.py`

Responsable: D.

```python
MODOS = ("sin_lock", "con_lock", "semaforo")


@dataclass(frozen=True)
class ResultadoConcurrencia:
    modo: str
    valor_esperado: int
    valor_obtenido: int
    correcto: bool
    detalle: str
```

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `ejecutar_concurrencia` | `ejecutar_concurrencia(modo: str, hilos: int = 4, iteraciones: int = 1000) -> ResultadoConcurrencia` | Resultado de la demostracion. |

Stub T1.3: valida el modo y devuelve resultados falsos. `sin_lock` simula un
resultado incorrecto; `con_lock` y `semaforo` simulan resultados correctos. La
implementacion con hilos reales corresponde a T3.11.

## 13. `mensajes.py`

Responsable: C.

| Simbolo | Firma | Devuelve o uso |
|---|---|---|
| `enviar` | `enviar(texto: str) -> None` | Agrega un mensaje al final de la cola. |
| `recibir` | `recibir() -> str \| None` | Mensaje mas antiguo, o `None` si no hay. |
| `cantidad` | `cantidad() -> int` | Cantidad de mensajes pendientes. |
| `limpiar` | `limpiar() -> None` | Vacía la cola. |

Stub T1.3: `enviar` y `limpiar` no hacen nada; `recibir` devuelve `None` y
`cantidad` devuelve `0`. La cola FIFO real corresponde a T3.10.

## 14. `main.py`

Responsable: C. Ya implementado en T2.1; no se modifica en T1.3.

| Simbolo | Firma | Uso actual |
|---|---|---|
| `limpiar_pantalla` | `limpiar_pantalla() -> None` | Limpia la terminal con `cls` o `clear`. |
| `mostrar_tokens` | `mostrar_tokens(tokens: list[Token]) -> None` | Imprime tipo, lexema y columna. |
| `ejecutar_linea` | `ejecutar_linea(linea: str) -> bool` | Procesa una linea; `False` termina el bucle. |
| `main` | `main() -> None` | Bucle principal de la consola. |

## 15. Comportamiento de los stubs

| Aspecto | Regla |
|---|---|
| Importacion | Todos los modulos se importan sin dependencias externas ni ciclos. |
| Datos | Los stubs devuelven listas vacias, `None`, valores por defecto o datos falsos documentados. |
| Errores | Solo se lanzan `ValueError` en validaciones simples del contrato. |
| Efectos secundarios | No se crean archivos, no se reserva memoria real, no se lanzan hilos ni se planifica de verdad. |
| Consola | `main.py` sigue funcionando porque `lexer.tokenizar` mantiene un tokenizador falso. |
| Reemplazo | Cada stub se sustituye en su tarea de implementacion de la fase 3 o 4. |

## 16. Verificacion de T1.3

La comprobacion minima es:

```bash
python3 - <<'PY'
import tokens, lexer, parser, consola
import procesos, planificador, estadisticas
import memoria, archivos, hilos_sync, mensajes
print("imports OK")
PY
```

Tambien se verifica que `python3 main.py` siga arrancando y que una linea
simple produzca tokens sin errores.

## 17. Criterios de aceptacion

- [x] Documento de firmas creado.
- [x] `tokens.py` con estructuras y constantes declaradas.
- [x] `lexer.py` con `Token` y `tokenizar` importables.
- [x] `parser.py` con `Orden` y `parsear` importables.
- [x] `consola.py` con `despachar` y `ayuda` importables.
- [x] `procesos.py` con `EstadoProceso`, `Proceso` y funciones de gestion.
- [x] `planificador.py` con estructuras y funciones de los tres algoritmos.
- [x] `estadisticas.py` con calculo y formato.
- [x] `memoria.py` con reserva, liberacion y estado.
- [x] `archivos.py` con operaciones basicas.
- [x] `hilos_sync.py` con el contrato de concurrencia.
- [x] `mensajes.py` con la cola FIFO.
- [x] Todos los stubs se importan sin error.
