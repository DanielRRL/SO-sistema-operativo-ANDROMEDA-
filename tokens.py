"""Tabla central de palabras reservadas y terminales del simulador."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DefinicionToken:
    """Describe una palabra o clase de token del lenguaje."""

    palabra: str
    tipo: str
    definicion: str
    ejemplo: str
    sintaxis: str = ""


_DEFINICIONES: dict[str, tuple[str, str, str]] = {
    "crear": ("CREAR", "Crea un proceso nuevo o un archivo dentro de carpeta_pruebas.", "crear proceso editor llegada=0 cpu=8 prioridad=2 mem=128"),
    "listar": ("LISTAR", "Lista los procesos registrados o los archivos de carpeta_pruebas.", "listar procesos"),
    "consultar": ("CONSULTAR", "Muestra los datos de un proceso.", "consultar proceso 1"),
    "finalizar": ("FINALIZAR", "Marca un proceso como terminado y libera su memoria.", "finalizar proceso 1"),
    "planificar": ("PLANIFICAR", "Ejecuta un algoritmo de planificación sobre los procesos listos.", "planificar sjf"),
    "estadisticas": ("ESTADISTICAS", "Muestra los tiempos y promedios de la última planificación.", "estadisticas"),
    "concurrencia": ("CONCURRENCIA", "Ejecuta la demostración de hilos sobre un recurso compartido.", "concurrencia con_lock"),
    "mensaje": ("MENSAJE", "Trabaja con la cola FIFO de mensajes.", "mensaje enviar \"listo\""),
    "memoria": ("MEMORIA", "Consulta o modifica la memoria simulada.", "memoria estado"),
    "archivo": ("ARCHIVO", "Inicia una operación sobre archivos.", "archivo listar"),
    "ejemplo": ("EJEMPLO", "Carga los cuatro procesos de ejemplo.", "ejemplo"),
    "ayuda": ("AYUDA", "Muestra la ayuda general o la de una palabra.", "ayuda planificar"),
    "tokens": ("TOKENS", "Muestra los tokens reconocidos en el resto de la línea.", "tokens crear proceso @x"),
    "limpiar": ("LIMPIAR", "Limpia la pantalla de la consola.", "limpiar"),
    "salir": ("SALIR", "Termina el simulador.", "salir"),
    "proceso": ("PROCESO", "Objeto proceso en singular.", "consultar proceso 2"),
    "procesos": ("PROCESOS", "Objeto proceso en plural.", "listar procesos"),
    "asignar": ("ASIGNAR", "Reserva memoria para un proceso.", "memoria asignar 1 256"),
    "liberar": ("LIBERAR", "Libera la memoria de un proceso.", "memoria liberar 1"),
    "estado": ("ESTADO", "Muestra el estado de la memoria.", "memoria estado"),
    "enviar": ("ENVIAR", "Agrega un mensaje al final de la cola.", "mensaje enviar \"hola\""),
    "recibir": ("RECIBIR", "Saca el mensaje más antiguo de la cola.", "mensaje recibir"),
    "leer": ("LEER", "Muestra el contenido de un archivo.", "archivo leer notas.txt"),
    "modificar": ("MODIFICAR", "Agrega texto al final de un archivo.", "archivo modificar notas.txt \"otra linea\""),
    "eliminar": ("ELIMINAR", "Borra un archivo de carpeta_pruebas.", "archivo eliminar notas.txt"),
    "fcfs": ("FCFS", "Primero en llegar, primero en ser atendido.", "planificar fcfs"),
    "sjf": ("SJF", "Trabajo más corto primero, no expulsivo.", "planificar sjf"),
    "rr": ("RR", "Round Robin con turnos de quantum.", "planificar rr quantum=3"),
    "sin_lock": ("SIN_LOCK", "Hilos sin protección; muestra una condición de carrera.", "concurrencia sin_lock"),
    "con_lock": ("CON_LOCK", "Hilos protegidos con Lock.", "concurrencia con_lock"),
    "semaforo": ("SEMAFORO", "Hilos protegidos con Semaphore.", "concurrencia semaforo"),
    "llegada": ("LLEGADA", "Instante de llegada del proceso.", "llegada=2"),
    "cpu": ("CPU", "Tiempo total de CPU requerido.", "cpu=8"),
    "prioridad": ("PRIORIDAD", "Prioridad del proceso; menor número es mayor prioridad.", "prioridad=1"),
    "mem": ("MEM", "Memoria requerida por el proceso en MB.", "mem=128"),
    "quantum": ("QUANTUM", "Tiempo máximo de CPU por turno en Round Robin.", "quantum=3"),
    "id": ("ID", "Nombre de proceso con letras, dígitos y guion bajo.", "editor"),
    "nombre_archivo": ("NOMBRE_ARCHIVO", "Nombre de archivo con extensión, sin rutas.", "notas.txt"),
    "numero": ("NUMERO", "Entero no negativo.", "128"),
    "cadena": ("CADENA", "Texto entre comillas dobles; el lexema no incluye las comillas.", "\"hola mundo\""),
    "igual": ("IGUAL", "Separa un atributo de su valor.", "cpu=8"),
    "fin": ("FIN", "Marca el final de la entrada.", "(automático)"),
    "error": ("ERROR", "Carácter o secuencia no reconocida.", "@"),
}

_CLASES = {"id", "nombre_archivo", "numero", "cadena", "igual", "fin", "error"}

PALABRAS_RESERVADAS: dict[str, str] = {
    palabra: tipo
    for palabra, (tipo, _, _) in _DEFINICIONES.items()
    if palabra not in _CLASES
}
PALABRAS: tuple[str, ...] = tuple(PALABRAS_RESERVADAS)
RESERVADAS: dict[str, str] = PALABRAS_RESERVADAS
SIMBOLOS: dict[str, str] = {"=": "IGUAL"}

TERMINALES: dict[str, DefinicionToken] = {
    palabra: DefinicionToken(palabra, tipo, definicion, ejemplo)
    for palabra, (tipo, definicion, ejemplo) in _DEFINICIONES.items()
}


def buscar_definicion(palabra: str) -> DefinicionToken | None:
    """Devuelve la definición de una palabra, o None si no existe."""
    return TERMINALES.get(palabra.lower())


def listar_definiciones() -> list[DefinicionToken]:
    """Devuelve todas las definiciones registradas."""
    return list(TERMINALES.values())


__all__ = [
    "DefinicionToken",
    "PALABRAS",
    "PALABRAS_RESERVADAS",
    "RESERVADAS",
    "SIMBOLOS",
    "TERMINALES",
    "buscar_definicion",
    "listar_definiciones",
]
