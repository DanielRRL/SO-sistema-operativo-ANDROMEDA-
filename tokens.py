from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    columna: int

    def __repr__(self):
        return f"Token(tipo={self.tipo!r}, valor={self.valor!r}, linea={self.linea}, columna={self.columna})"


PALABRAS_RESERVADAS = {
    "crear": "CREAR",
    "listar": "LISTAR",
    "consultar": "CONSULTAR",
    "finalizar": "FINALIZAR",
    "planificar": "PLANIFICAR",
    "fcfs": "FCFS",
    "sjf": "SJF",
    "rr": "RR",
    "estadisticas": "ESTADISTICAS",
    "memoria": "MEMORIA",
    "archivo": "ARCHIVO",
    "leer": "LEER",
    "modificar": "MODIFICAR",
    "eliminar": "ELIMINAR",
    "hilos": "HILOS",
    "sin_lock": "SIN_LOCK",
    "con_lock": "CON_LOCK",
    "semaforo": "SEMAFORO",
    "mensaje": "MENSAJE",
    "enviar": "ENVIAR",
    "recibir": "RECIBIR",
    "ayuda": "AYUDA",
    "tokens": "TOKENS",
    "limpiar": "LIMPIAR",
    "salir": "SALIR",
}

SIMBOLOS = {
    "(": "PAREN_ABRE",
    ")": "PAREN_CIERRA",
    ",": "COMA",
    ";": "PUNTO_COMA",
}

TOKEN_DEFINICION = {
    "CREAR": ("crear", "Comando para crear un proceso", "crear editor 0 5 2 128"),
    "LISTAR": ("listar", "Lista procesos o elementos del módulo correspondiente", "listar"),
    "CONSULTAR": ("consultar", "Consulta un proceso por pid", "consultar 1"),
    "FINALIZAR": ("finalizar", "Finaliza un proceso por pid", "finalizar 1"),
    "PLANIFICAR": ("planificar", "Ejecuta un algoritmo de planificación", "planificar rr 2"),
    "FCFS": ("fcfs", "Algoritmo First-Come, First-Served", "planificar fcfs"),
    "SJF": ("sjf", "Algoritmo Shortest Job First", "planificar sjf"),
    "RR": ("rr", "Round Robin con quantum configurable", "planificar rr 3"),
    "ESTADISTICAS": ("estadisticas", "Muestra métricas y promedios", "estadisticas"),
    "MEMORIA": ("memoria", "Consulta el estado de la memoria simulada", "memoria"),
    "ARCHIVO": ("archivo", "Inicia una operación sobre archivos", "archivo listar"),
    "LEER": ("leer", "Lee el contenido de un archivo", "archivo leer nota.txt"),
    "MODIFICAR": ("modificar", "Modifica el contenido de un archivo", "archivo modificar nota.txt \"nuevo\""),
    "ELIMINAR": ("eliminar", "Elimina un archivo dentro de carpeta_pruebas", "archivo eliminar nota.txt"),
    "HILOS": ("hilos", "Ejecuta la demostración de concurrencia", "hilos con_lock"),
    "SIN_LOCK": ("sin_lock", "Modo de hilos sin sincronización", "hilos sin_lock"),
    "CON_LOCK": ("con_lock", "Modo de hilos con bloqueo", "hilos con_lock"),
    "SEMAFORO": ("semaforo", "Modo de hilos con semáforo", "hilos semaforo"),
    "MENSAJE": ("mensaje", "Inicia una operación sobre mensajes", "mensaje enviar \"listo\""),
    "ENVIAR": ("enviar", "Envía un mensaje a la cola", "mensaje enviar \"listo\""),
    "RECIBIR": ("recibir", "Lee un mensaje de la cola", "mensaje recibir"),
    "AYUDA": ("ayuda", "Muestra información de un comando", "ayuda planificar"),
    "TOKENS": ("tokens", "Muestra la lista de tokens reconocidos", "tokens"),
    "LIMPIAR": ("limpiar", "Limpia la pantalla de la consola", "limpiar"),
    "SALIR": ("salir", "Cierra la aplicación", "salir"),
    "ID": ("identificador", "Nombre de proceso o archivo", "editor o nota.txt"),
    "NUMERO": ("numero", "Número entero", "128 o 3"),
    "CADENA": ("cadena", "Texto entre comillas dobles", "\"hola\""),
    "FIN": ("fin_de_linea", "Fin del comando o instrucción", "nueva línea"),
}

TOKEN_TABLE = [
    {"palabra": palabra, "token": token, "definicion": definicion, "ejemplo": ejemplo}
    for token, (palabra, definicion, ejemplo) in TOKEN_DEFINICION.items()
]

__all__ = [
    "Token",
    "PALABRAS_RESERVADAS",
    "SIMBOLOS",
    "TOKEN_DEFINICION",
    "TOKEN_TABLE",
]
