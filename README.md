# Simulador de Sistema Operativo ANDROMEDA

Simulador didáctico de un sistema operativo con interfaz por línea de comandos,
desarrollado en Python puro para Linux. El usuario escribe una orden, el lexer la
convierte en tokens, el parser valida la gramática y el despachador ejecuta la
acción correspondiente en los módulos del simulador.

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

Modo script previsto:

```bash
python3 main.py --script pruebas/demo.txt
```

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

- Escribir los comandos en minúsculas y sin tildes:
  `crear`, `listar`, `consultar`, `finalizar`, `planificar`, `estadisticas`,
  `concurrencia`, `mensaje`, `memoria`, `archivo`, `ejemplo`, `ayuda`,
  `tokens`, `limpiar`, `salir`.
- Aunque el lexer reconoce las palabras reservadas sin distinguir mayúsculas,
  la forma oficial y documentada es minúsculas.
- Escribir una orden por línea.
- Permitir espacios adicionales entre tokens.
- Ante un comando mal escrito, responder con el uso correcto.

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
```
