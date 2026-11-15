"""Cola FIFO de mensajes del simulador (T3.10).

Usa queue.Queue de la biblioteca estandar: es segura entre hilos, asi que un
hilo puede enviar mensajes mientras otro los recibe sin necesidad de un Lock
propio. FIFO significa que el primer mensaje que entra es el primero que sale.
"""

import queue

# Una sola cola para todo el simulador (estado del modulo).
_cola: "queue.Queue[str]" = queue.Queue()


def enviar(texto: str) -> None:
    """Agrega un mensaje al final de la cola."""
    _cola.put(texto)


def recibir() -> str | None:
    """Saca y devuelve el mensaje mas antiguo, o None si la cola esta vacia.

    No bloquea: si no hay mensajes responde de inmediato con None.
    """
    try:
        return _cola.get_nowait()
    except queue.Empty:
        return None


def cantidad() -> int:
    """Devuelve la cantidad de mensajes pendientes."""
    return _cola.qsize()


def limpiar() -> None:
    """Vacia la cola de mensajes."""
    while recibir() is not None:
        pass