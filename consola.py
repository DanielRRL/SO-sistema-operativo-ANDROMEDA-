"""Despachador de ordenes de la consola. Stub temporal de T1.3."""

from parser import Orden


def despachar(orden: Orden) -> str:
    """Ejecuta una orden y devuelve el mensaje para la consola."""
    return f"[ERROR] Despacho pendiente para el comando '{orden.comando}'."


def ayuda(palabra: str | None = None) -> str:
    """Devuelve la ayuda general o la ayuda de una palabra."""
    if palabra:
        return f"[ERROR] Ayuda pendiente para '{palabra}'."
    return "[ERROR] Ayuda pendiente."
