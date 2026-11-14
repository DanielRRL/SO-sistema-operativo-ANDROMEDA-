# T1.1 - Terminales y sintaxis

Proyecto: Simulación de un sistema operativo  
Sistema operativo: Sistemas Operativos  
Ingeniería de Software (EAM)  
Responsable: Persona B (Lexer, memoria y archivos)  
Fase 1 - Diseño  
Propuesta para cerrar con el equipo

## 1. Convenciones

- Python 3.10 o superior.
- Solo biblioteca estándar.
- Comandos en minúsculas y sin tildes.
- Los tokens del lenguaje se nombran en mayúsculas para la especificación, pero la sintaxis ejecutable usa minúsculas.
- Mensajes de salida con el prefijo `[OK]` o `[ERROR]`.
- Memoria simulada total: 1024 MB.
- Quantum de Round Robin por defecto: 3.
- Los archivos se manejan solo dentro de `carpeta_pruebas`.

## 2. Lista de comandos

| Módulo | Comando | Ejemplo |
|---|---|---|
| Procesos | `crear <nombre> <llegada> <cpu> <prioridad> <memoria>` | `crear editor 0 5 2 128` |
| Procesos | `listar` | `listar` |
| Procesos | `consultar <pid>` | `consultar 1` |
| Procesos | `finalizar <pid>` | `finalizar 1` |
| Planificación | `planificar fcfs` | `planificar fcfs` |
| Planificación | `planificar sjf` | `planificar sjf` |
| Planificación | `planificar rr [quantum]` | `planificar rr 2` |
| Estadísticas | `estadisticas` | `estadisticas` |
| Memoria | `memoria` (muestra usada y libre) | `memoria` |
| Archivos | `archivo crear <nombre> "<texto>"` | `archivo crear nota.txt "hola"` |
| Archivos | `archivo listar` | `archivo listar` |
| Archivos | `archivo leer <nombre>` | `archivo leer nota.txt` |
| Archivos | `archivo modificar <nombre> "<texto>"` | `archivo modificar nota.txt "nuevo"` |
| Archivos | `archivo eliminar <nombre>` | `archivo eliminar nota.txt` |
| Hilos | `hilos sin_lock` | `hilos sin_lock` |
| Hilos | `hilos con_lock` | `hilos con_lock` |
| Hilos | `hilos semaforo` | `hilos semaforo` |
| Mensajes | `mensaje enviar "<texto>"` | `mensaje enviar "listo"` |
| Mensajes | `mensaje recibir` | `mensaje recibir` |
| Utilidades | `ayuda [comando]` | `ayuda planificar` |
| Utilidades | `tokens` | `tokens` |
| Utilidades | `limpiar` | `limpiar` |
| Utilidades | `salir` | `salir` |

Nota: `listar` y `archivo listar` son comandos distintos; el primero actúa sobre procesos y el segundo sobre archivos.

La asignación y liberación de memoria no tiene comando propio: se hace al crear (reserva) y al finalizar (libera).

## 3. Terminales (tokens)

| Token | Patrón o palabra | Uso |
|---|---|---|
| `CREAR`, `LISTAR`, `CONSULTAR`, `FINALIZAR` | palabra exacta | Comandos de procesos |
| `PLANIFICAR`, `FCFS`, `SJF`, `RR` | palabra exacta | Planificación |
| `ESTADISTICAS`, `MEMORIA` | palabra exacta | Estadísticas y memoria |
| `ARCHIVO`, `LEER`, `MODIFICAR`, `ELIMINAR` | palabra exacta | Archivos |
| `HILOS`, `SIN_LOCK`, `CON_LOCK`, `SEMAFORO` | palabra exacta | Concurrencia y sincronización |
| `MENSAJE`, `ENVIAR`, `RECIBIR` | palabra exacta | Cola de mensajes |
| `AYUDA`, `TOKENS`, `LIMPIAR`, `SALIR` | palabra exacta | Utilidades |
| `NUMERO` | `[0-9]+` | `pid`, llegada, CPU, prioridad, memoria, quantum |
| `ID` | `[A-Za-z_][A-Za-z0-9_.]*` | Nombre de proceso o de archivo |
| `CADENA` | texto entre comillas dobles | Contenido de archivos y mensajes |
| `FIN` | fin de línea | Cierre del comando |

Un carácter que no encaje en ningún token debe reportarse como `[ERROR]` indicando el carácter y su columna.

## 4. Gramática (EBNF)

```ebnf
linea        ::= comando FIN
comando      ::= CREAR ID NUMERO NUMERO NUMERO NUMERO
               | LISTAR
               | CONSULTAR NUMERO
               | FINALIZAR NUMERO
               | PLANIFICAR algoritmo
               | ESTADISTICAS
               | MEMORIA
               | ARCHIVO accion_arch
               | HILOS modo
               | MENSAJE accion_msg
               | AYUDA [ID | palabra_clave]
               | TOKENS
               | LIMPIAR
               | SALIR
algoritmo    ::= FCFS | SJF | RR [NUMERO]
accion_arch  ::= CREAR ID CADENA
               | LISTAR
               | LEER ID
               | MODIFICAR ID CADENA
               | ELIMINAR ID
modo         ::= SIN_LOCK | CON_LOCK | SEMAFORO
accion_msg   ::= ENVIAR CADENA | RECIBIR
```

## 5. Puntos para cerrar con el equipo

- El `pid` lo asigna el simulador automáticamente (`1, 2, 3...`) y `crear` lo muestra en el `[OK]`.
- Orden de los campos de `crear`: nombre, llegada, cpu, prioridad, memoria (como en el enunciado).
- `ayuda <comando>` acepta palabras clave aunque sean terminales. Por ejemplo: `ayuda planificar`, `ayuda archivo`, `ayuda tokens`.
- Casos de error que el parser cubre con el uso correcto: faltan argumentos, sobran argumentos, `rr` con quantum 0 y rutas con `..` en archivos.

## 6. Resumen de la sintaxis funcional

```text
crear <nombre> <llegada> <cpu> <prioridad> <memoria>
listar
consultar <pid>
finalizar <pid>
planificar fcfs
planificar sjf
planificar rr [quantum]
estadisticas
memoria
archivo crear <nombre> "<texto>"
archivo listar
archivo leer <nombre>
archivo modificar <nombre> "<texto>"
archivo eliminar <nombre>
hilos sin_lock
hilos con_lock
hilos semaforo
mensaje enviar "<texto>"
mensaje recibir
ayuda [comando]
tokens
limpiar
salir
```
