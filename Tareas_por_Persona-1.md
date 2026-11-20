## Tareas por persona

Cada tarea aparece una sola vez, con un único responsable. Los IDs son los del plan de trabajo. Depende de = lo que debe estar listo antes de empezar (entre paréntesis, quién lo hace).

Fases: 0 Arranque · 1 Diseño · 2 Esqueleto · 3 Desarrollo · 4 Integración · 5 Pruebas · 6 Documentación · 7 Sustentación.

Empiecen por: T0.1 (todos), T0.2 (C), T1.1 (B) y T1.2 (A, después de T0.3). De ellas depende que los demás puedan avanzar. Mientras una dependencia no esté lista, trabajen con datos falsos (stubs).

## Todos Tareas de todo el equipo (se hacen juntos, una sola vez)

| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T0.1 | Reunión de arranque | 0 Arranque | - |
|   | Confirmar roles, canal de comunicación y fechas (entrega, hitos |   |   |
|   | y ensayos). |   |   |
| T1.3 | Firmas y stubs | 1 Diseño | T1.1 (B), T1.2 (A) |
|   | Cada uno define las funciones de sus archivos (nombre, |   |   |
|   | parámetros, qué devuelve) y las deja como stubs que se |   |   |
|   | importan sin error. |   |   |
| T4.4 | Recorrido completo | 4 Integración | T4.1 (C), T4.2 (A), T4.3 (C) |
|   | Correr juntos la sesión de ejemplo; cada uno corrige lo suyo |   |   |
|   | hasta que no falle nada. |   |   |
| T5.5 | Revisión cruzada de código | 5 Pruebas | T4.4 (todos) |
|   | A revisa a B, B revisa a C, C revisa a D y D revisa a A. |   |   |
| T7.1 | Guión y ensayos | 7 Sustentación | T6.5 (B) |
|   | Ajustar el guión de la demo y hacer 2 ensayos; en el segundo, |   |   |
|   | cada uno explica el módulo de otro. |   |   |

## Persona A Núcleo: procesos, planificación y estadísticas

| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T0.3 | Convenciones | 0 Arranque | T0.1 (todos) |
|   | Python 3.10+, solo biblioteca estándar, comandos sin tildes, |   |   |
|   | mensajes [OK] y [ERROR]. Dejarlo en el README. |   |   |
| T1.2 | Contrato de Proceso | 1 Diseño | T0.3 (A) |
|   | Campos (pid, nombre, llegada, cpu, prioridad, memoria, |   |   |
|   | estado), estados y qué devuelven los planificadores (lista con |   |   |
|   | tiempos y Gantt). |   |   |
| T1.5 | Pseudocódigo FCFS, SJF y RR | 1 Diseño | T1.2 (A) |
|   | Con su diagrama de flujo, probado a mano con P1 a P4. |   |   |
| T1.6 | Borrador del documento de diseño | 1 Diseño | T1.3 (todos), T1.4 (D) |
|   | Problema, objetivos, arquitectura y descripción de módulos. |   |   |
| T3.1 | procesos.py | 3 Desarrollo | T1.2 (A), T1.3 (todos) |
|   | Clase Proceso; crear, listar, consultar y finalizar. |   |   |
| T3.2 | FCFS y SJF no expulsivo | 3 Desarrollo | T1.5 (A), T3.1 (A) |
|   | Con diagrama de Gantt. |   |   |
| T3.3 | Round Robin | 3 Desarrollo | T3.2 (A) |
|   | Quantum configurable (por defecto 3). |   |   |


| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T3.4 | estadisticas.py | 3 Desarrollo | T3.2 (A) |
|   | Finalización, retorno, espera y promedios. |   |   |
| T4.2 | Conectar memoria con procesos | 4 Integración | T3.1 (A), T3.7 (B) |
|   | Al crear se reserva; si no hay espacio queda Rechazado; al |   |   |
|   | finalizar se libera. |   |   |
| T5.2 | Pruebas de algoritmos | 5 Pruebas | T3.3 (A), T3.4 (A) |
|   | Datos de ejemplo y casos borde (un solo proceso, CPU ociosa, |   |   |
|   | quantum 1). |   |   |
| T6.1 | Documento de diseño final | 6 | T1.6 (A), T6.6 (B) |
|   | Unir todo e incluir el anexo léxico de B. | Documentación |   |

## Persona B Lexer, memoria y archivos

| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T1.1 | Terminales y sintaxis | 1 Diseño | T0.1 (todos) |
|   | Cerrar con los demás la lista de comandos y la gramática |   |   |
|   | (secciones 6 y 7 del plan). |   |   |
| T2.3 | tokens.py | 2 Esqueleto | T1.1 (B) |
|   | Tabla con palabra, token, definición y ejemplo de cada terminal. |   |   |
| T3.5 | lexer.py | 3 Desarrollo | T2.3 (B) |
|   | Función tokenizar (código base del plan), con errores y |   |   |
|   | columna. |   |   |
| T3.6 | Comandos ayuda y tokens | 3 Desarrollo | T3.5 (B) |
|   | ayuda muestra definición y ejemplo; tokens muestra lo que |   |   |
|   | reconoce el lexer. |   |   |
| T3.7 | memoria.py | 3 Desarrollo | T1.3 (todos) |
|   | Asignar y liberar validando la capacidad (1024 MB). |   |   |
| T3.8 | archivos.py | 3 Desarrollo | T1.3 (todos) |
|   | Crear, listar, leer, modificar y eliminar, solo dentro de |   |   |
|   | carpeta_pruebas. |   |   |
| T5.1 | Pruebas del lexer | 5 Pruebas | T3.5 (B) |
|   | Al menos 25 casos válidos e inválidos. |   |   |
| T6.5 | README | 6 | T5.6 (C) |
|   | Cómo ejecutar, lista de comandos y un ejemplo. | Documentación |   |
| T6.6 | Anexo de especificación léxica | 6 | T5.6 (C) |
|   | Terminales, patrones y gramática, para el documento de | Documentación |   |
|   | diseño. |   |   |

## Persona C Parser, consola e integración

| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T0.2 | Crear el repositorio | 0 Arranque | T0.1 (todos) |
|   | Estructura de carpetas, README mínimo y acceso para los 4. |   |   |
| T0.5 | Confirmar con el docente | 0 Arranque | T0.1 (todos) |
|   | Si la consola con ayuda cuenta como menú integrado y cuánto |   |   |
|   | dura la sustentación. |   |   |


| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T2.1 | main.py esqueleto | 2 Esqueleto | T0.2 (C) |
|   | Bucle de lectura que imprime tokens falsos; soporta salir y |   |   |
|   | limpiar sin errores técnicos. |   |   |
| T3.10 | mensajes.py | 3 Desarrollo | T1.3 (todos) |
|   | Cola de mensajes con enviar y recibir. |   |   |
| T3.9 | parser.py | 3 Desarrollo | T1.1 (B), T1.3 (todos) |
|   | Valida la gramática y muestra el uso correcto ante errores. |   |   |
| T4.1 | Despachador (consola.py) | 4 Integración | T3.1 a T3.11 (Fase 3) |
|   | Conecta cada comando con su módulo y reemplaza los stubs. |   |   |
| T4.3 | Modo script | 4 Integración | T4.1 (C) |
|   | python main.py --script archivo y pruebas/demo.txt |   |   |
|   | con la sesión de ejemplo. |   |   |
| T5.3 | Pruebas de casos de error | 5 Pruebas | T4.1 (C) |
|   | Comando mal escrito, pid inexistente, memoria insuficiente, |   |   |
|   | ruta con "..": nunca debe verse un error técnico. |   |   |
| T5.6 | Congelar la versión | 5 Pruebas | T5.1 (B), T5.2 (A), T5.3 (C), |
|   | Etiqueta v1.0 o ZIP; desde ahí solo se corrigen errores graves. |   | T5.4 (D), T5.5 (todos) |

## Persona D Concurrencia, Linux y documentación

| ID | Tarea | Fase | Depende de |
| --- | --- | --- | --- |
| T1.4 | Diagrama modular y de flujo | 1 Diseño | T1.1 (B), T1.3 (todos) |
|   | Módulos y flujo de la consola (entrada, lexer, parser, |   |   |
|   | despachador, módulos, salida). |   |   |
| T3.11 | hilos_sync.py | 3 Desarrollo | T1.3 (todos) |
|   | 3 hilos sobre un contador en los modos sin_lock, con_lock y |   |   |
|   | semaforo, mostrando valor esperado y obtenido. |   |   |
| T3.12 | Prácticas de Linux | 3 Desarrollo | T0.1 (todos) |
|   | Procesos, prioridades, hilos y permisos, con capturas y 2 o 3 |   |   |
|   | líneas de explicación cada una. |   |   |
| T5.4 | Pruebas de extremo a extremo | 5 Pruebas | T4.3 (C) |
|   | Correr demo.txt y guardar las capturas. |   |   |
| T6.2 | Actualizar el diagrama modular | 6 | T1.4 (D), T5.6 (C) |
|   | Con lo que realmente quedó implementado. | Documentación |   |
| T6.3 | Evidencias Linux y comparación | 6 | T3.12 (D), T5.4 (D) |
|   | Capturas explicadas y tabla simulación vs Linux con lo | Documentación |   |
|   | observado. |   |   |
| T6.4 | Informe final | 6 | T5.6 (C) |
|   | Pruebas, resultados, dificultades (cada uno aporta 3 o 4 líneas) | Documentación |   |
|   | y conclusiones. |   |   |
| T7.3 | Plan B de la demo | 7 Sustentación | T5.6 (C) |
|   | Video o capturas, y copia del proyecto en USB y nube. |   |   |
