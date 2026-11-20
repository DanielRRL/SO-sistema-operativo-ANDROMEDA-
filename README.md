# Simulador de Sistema Operativo ANDROMEDA

Simulador didáctico de un sistema operativo con interfaz por línea de comandos,
desarrollado en Python puro para Linux. El usuario escribe una orden, el lexer la
convierte en tokens y el parser valida la gramática. `ayuda` y `tokens` muestran
su salida correspondiente; los demás comandos se representan como órdenes
estructuradas mientras se completa su integración con el despachador.

## Requisitos

- Linux como sistema objetivo.
- Python 3.10 o superior.
- Solo biblioteca estándar de Python.
- Sin frameworks, paquetes externos ni instalaciones con `pip`.
- Sin interfaz gráfica: toda la interacción se realiza por terminal.

## Ejecución

```bash
python3 main.py
```

Modo script:

```bash
python3 main.py --script pruebas/demo.txt
```

El archivo de demostración contiene una sesión con ejemplos de los comandos
del proyecto.

## Convenciones obligatorias

### Código

- Usar Python 3.10 o superior.
- Usar únicamente la biblioteca estándar: `re`, `dataclasses`, `threading`,
  `queue`, `os`, `unittest`, entre otros módulos nativos.
- No usar frameworks ni dependencias externas como Flask, Django, rich,
  colorama, pandas, numpy, tkinter o pygame.
- Mantener un diseño sencillo y vanilla, sin capas innecesarias.
- Seguir PEP 8: 4 espacios por nivel, nombres claros y líneas legibles.
- Guardar los archivos en UTF-8 y con saltos de línea LF.
- Mantener el código comentado donde la lógica no sea evidente.
- No depender de colores ANSI; la salida debe funcionar en una terminal simple.

### Consola

- El prompt fijo es `simulador> `.
- Leer con `input()` e imprimir con `print()`.
- No abrir ventanas ni usar interfaces gráficas.
- Mostrar tablas de texto alineadas con `ljust`, `rjust` o f-strings.
- Ignorar líneas vacías sin generar errores.
- Manejar `Ctrl+C` sin imprimir un traceback.
- El programa nunca debe caerse por una entrada inválida.

### Comandos

- Escribir los comandos en minúsculas y sin tildes. El lexer también reconoce
  las palabras reservadas en mayúsculas.
- Escribir una orden por línea.
- Permitir espacios adicionales entre tokens.
- Ante un comando mal escrito, responder con el uso correcto.

Sintaxis reconocida por el parser:

```text
crear proceso <nombre> cpu=<n> [llegada=<n>] [prioridad=<n>] [mem=<n>]
listar procesos
consultar proceso <pid>
finalizar proceso <pid>
planificar fcfs
planificar sjf
planificar rr [quantum=<n>]
estadisticas
concurrencia sin_lock | concurrencia con_lock | concurrencia semaforo
mensaje enviar "<texto>"
mensaje recibir
memoria estado
memoria asignar <pid> <mb>
memoria liberar <pid>
archivo crear <nombre.ext> ["<texto>"]
archivo listar
archivo leer <nombre.ext>
archivo modificar <nombre.ext> "<texto>"
archivo eliminar <nombre.ext>
ejemplo
ayuda [palabra]
tokens [entrada]
limpiar
salir
```

### Ejemplos de `ayuda` y `tokens`

Inicia el simulador con `python3 main.py` y escribe los comandos en el prompt
`simulador> `:

```text
simulador> ayuda
```

Muestra los comandos principales disponibles. Para consultar la descripción y
un ejemplo de un comando específico:

```text
simulador> ayuda planificar
```

El comando `tokens`, sin argumentos, muestra la tabla de terminales que reconoce
el lexer. También puedes escribir texto después de `tokens` para ver cómo se
clasifican sus elementos:

```text
simulador> tokens crear proceso @x
```

La salida muestra el tipo, el lexema y su posición. Los caracteres no
reconocidos aparecen con el tipo `ERROR`. Usa `salir` para cerrar el simulador.

Para recorrer la sesión de ejemplo y observar el análisis de las órdenes:

```bash
python3 main.py --script pruebas/demo.txt
```

En la versión actual, los comandos distintos de `ayuda`, `tokens`, `limpiar` y
`salir` se analizan y muestran como órdenes estructuradas; su ejecución completa
depende de conectar el despachador con los módulos.

La sintaxis completa, los terminales, sus patrones y la gramática se encuentran
en el [anexo de especificación léxica](docs/anexo_especificacion_lexica.md).

### Mensajes

- Usar `[OK]` al inicio de cada mensaje de éxito.
- Usar `[ERROR]` al inicio de cada mensaje de fallo.
- Acompañar siempre el mensaje con una explicación breve.
- No mostrar tracebacks al usuario.
- Ejemplos:
  - `[OK] Proceso 1 creado.`
  - `[ERROR] Memoria insuficiente para asignar 2000 MB.`

### Archivos

- Las operaciones del simulador solo pueden crear, leer, modificar o eliminar
  archivos dentro de `carpeta_pruebas/`.
- Rechazar rutas con `..`, rutas absolutas y cualquier intento de salir de
  `carpeta_pruebas/`.
- Validar la ruta final antes de ejecutar la operación.
- No usar nombres de archivo que coincidan con palabras reservadas.

### Pruebas

- Usar `unittest` de la biblioteca estándar.
- Probar cada módulo con al menos un caso válido y uno inválido.
- Ejecutar las pruebas con:

```bash
python3 -m unittest discover -s pruebas -v
```

La suite incluye más de 25 entradas válidas y más de 25 entradas léxicamente
inválidas para el lexer.

## Estructura del proyecto

```text
.
├── main.py
├── consola.py
├── tokens.py
├── lexer.py
├── parser.py
├── procesos.py
├── planificador.py
├── estadisticas.py
├── memoria.py
├── archivos.py
├── hilos_sync.py
├── mensajes.py
├── carpeta_pruebas/
├── pruebas/
│   ├── test_lexer.py
│   ├── test_planificador.py
│   └── demo.txt
└── docs/
    └── anexo_especificacion_lexica.md
```
