# Anexo: especificacion lexica y gramatical

Este anexo describe la entrada reconocida por `lexer.py` y la sintaxis que
valida `parser.py`. La tabla de palabras reservadas y sus definiciones está en
`tokens.py`.

## 1. Convenciones léxicas

- Las palabras reservadas se reconocen sin distinguir mayúsculas de
  minúsculas; se recomienda escribir los comandos en minúsculas.
- Los espacios, tabulaciones y retornos de carro separan tokens.
- La consola procesa una orden por línea. `FIN` marca el final del texto que se
  entrega a `tokenizar`; se agrega una sola vez, no por cada salto de línea.
- `#` inicia un comentario que continúa hasta el siguiente salto de línea,
  excepto cuando aparece dentro de una cadena entre comillas.
- Las posiciones de línea y columna empiezan en 1.
- El lexer conserva el lexema original y reporta errores como tokens `ERROR`,
  sin detener el análisis del resto del texto.

## 2. Terminales

### 2.1 Palabras reservadas

| Grupo | Palabras | Tipos de token |
|---|---|---|
| Procesos | `crear`, `listar`, `consultar`, `finalizar`, `proceso`, `procesos` | `CREAR`, `LISTAR`, `CONSULTAR`, `FINALIZAR`, `PROCESO`, `PROCESOS` |
| Planificación | `planificar`, `fcfs`, `sjf`, `rr`, `quantum` | `PLANIFICAR`, `FCFS`, `SJF`, `RR`, `QUANTUM` |
| Atributos de proceso | `llegada`, `cpu`, `prioridad`, `mem` | `LLEGADA`, `CPU`, `PRIORIDAD`, `MEM` |
| Memoria | `memoria`, `asignar`, `liberar`, `estado` | `MEMORIA`, `ASIGNAR`, `LIBERAR`, `ESTADO` |
| Archivos | `archivo`, `leer`, `modificar`, `eliminar` | `ARCHIVO`, `LEER`, `MODIFICAR`, `ELIMINAR` |
| Concurrencia | `concurrencia`, `sin_lock`, `con_lock`, `semaforo` | `CONCURRENCIA`, `SIN_LOCK`, `CON_LOCK`, `SEMAFORO` |
| Mensajes | `mensaje`, `enviar`, `recibir` | `MENSAJE`, `ENVIAR`, `RECIBIR` |
| Utilidades | `estadisticas`, `ejemplo`, `ayuda`, `tokens`, `limpiar`, `salir` | `ESTADISTICAS`, `EJEMPLO`, `AYUDA`, `TOKENS`, `LIMPIAR`, `SALIR` |

### 2.2 Patrones y símbolos

| Tipo | Patrón | Ejemplo | Descripción |
|---|---|---|---|
| `ID` | `[A-Za-z_][A-Za-z0-9_]*` | `editor_2` | Identificador que no sea una palabra reservada. |
| `NOMBRE_ARCHIVO` | `[A-Za-z0-9_-]+\.[A-Za-z0-9]+` | `notas.txt` | Nombre con una extensión; no admite directorios. |
| `NUMERO` | `[0-9]+` | `128` | Entero no negativo. |
| `CADENA` | Texto entre comillas dobles | `"hola mundo"` | El lexema del token no contiene las comillas. |
| `IGUAL` | `=` | `cpu=8` | Separa un atributo de su valor. |
| `FIN` | Fin del texto de entrada | — | Se agrega automáticamente al resultado. |
| `ERROR` | Cualquier carácter no reconocido o cadena sin cerrar | `@` | Incluye el lexema y su posición. |

Dentro de una cadena se reconocen los escapes `\"`, `\\`, `\n` y `\t`.
Una secuencia de escape desconocida se conserva literalmente. Una cadena que
no cierra antes de un salto de línea o del final del texto produce `ERROR`.

Los nombres de archivo se reconocen antes que identificadores y números. Por
eso `123.txt` es un `NOMBRE_ARCHIVO`, mientras que `123` es un `NUMERO`.

## 3. Gramática (EBNF)

`NUM` representa un token `NUMERO`, `ID` un identificador y `CADENA` un texto
entre comillas. Las llaves indican repetición y los corchetes, opcionalidad.

```ebnf
entrada            ::= [comando] [comentario] FIN

comando            ::= crear
                     | listar
                     | consultar
                     | finalizar
                     | planificar
                     | estadisticas
                     | concurrencia
                     | mensaje
                     | memoria
                     | archivo
                     | ejemplo
                     | ayuda
                     | tokens
                     | limpiar
                     | salir

crear              ::= CREAR PROCESO ID atributo { atributo }
atributo           ::= LLEGADA IGUAL NUM
                     | CPU IGUAL NUM
                     | PRIORIDAD IGUAL NUM
                     | MEM IGUAL NUM

listar             ::= LISTAR PROCESOS
consultar          ::= CONSULTAR PROCESO NUM
finalizar          ::= FINALIZAR PROCESO NUM

planificar         ::= PLANIFICAR (FCFS | SJF | RR [QUANTUM IGUAL NUM])
estadisticas       ::= ESTADISTICAS
concurrencia       ::= CONCURRENCIA (SIN_LOCK | CON_LOCK | SEMAFORO)

mensaje            ::= MENSAJE (ENVIAR CADENA | RECIBIR)

memoria            ::= MEMORIA [ESTADO
                     | ASIGNAR NUM NUM
                     | LIBERAR NUM]

archivo            ::= ARCHIVO (CREAR NOMBRE_ARCHIVO [CADENA]
                     | LISTAR
                     | LEER NOMBRE_ARCHIVO
                     | MODIFICAR NOMBRE_ARCHIVO CADENA
                     | ELIMINAR NOMBRE_ARCHIVO)

ejemplo            ::= EJEMPLO
ayuda              ::= AYUDA [palabra]
tokens             ::= TOKENS { cualquier_token }
limpiar            ::= LIMPIAR
salir              ::= SALIR

comentario         ::= "#" { cualquier_caracter_excepto_salto_de_linea }
palabra            ::= ID | palabra_reservada
```

La gramática se aplica a una línea por vez. Una línea vacía o con solo un
comentario no contiene un comando.

### 3.1 Restricciones semánticas del parser

- `crear proceso` requiere exactamente un atributo `cpu`; los atributos
  admitidos no pueden repetirse. `cpu` y `mem`, cuando se indican, deben ser
  mayores que cero.
- `llegada`, `prioridad` y `mem` son opcionales en la sintaxis; sus valores por
  defecto los determina el módulo de procesos.
- Si Round Robin no recibe `quantum`, se usa 3. El quantum explícito debe ser
  mayor que cero.
- `memoria` sin subcomando equivale a `memoria estado`.
- `tokens` acepta el resto de la entrada, incluidos tokens `ERROR`, para que
  puedan inspeccionarse.
- Los comandos que no declaran argumentos rechazan tokens sobrantes.
- Los errores sintácticos indican el uso esperado y, cuando aplica, la columna
  donde se encontró el problema.

## 4. Ejemplos léxicos

Entrada:

```text
crear proceso editor cpu=8 mem=128
```

Secuencia resumida:

```text
CREAR PROCESO ID CPU IGUAL NUMERO MEM IGUAL NUMERO FIN
```

Entrada con un carácter inválido:

```text
tokens crear proceso @x
```

El lexer produce un token `ERROR` para `@` y continúa reconociendo `x` como
`ID`. El comando `tokens` muestra los tipos, lexemas y posiciones resultantes.

## 5. Implementación y pruebas

- Palabras reservadas y metadatos: `tokens.py`.
- Tokenización y posiciones: `lexer.py`.
- Validación de la gramática y mensajes de uso: `parser.py`.
- Casos de prueba: `pruebas/test_lexer.py`.
- Ejecutar la suite: `python3 -m unittest discover -s pruebas -v`.
