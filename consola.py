"""Utilidades de ayuda y lexer usadas por los comandos de consola."""

from lexer import tokenizar
from parser import Orden
from tokens import buscar_definicion, listar_definiciones


_COMANDOS_PRINCIPALES = (
    "crear",
    "listar",
    "consultar",
    "finalizar",
    "planificar",
    "estadisticas",
    "concurrencia",
    "mensaje",
    "memoria",
    "archivo",
    "ejemplo",
    "ayuda",
    "tokens",
    "limpiar",
    "salir",
)


def ayuda(palabra: str | None = None) -> str:
    """Devuelve la ayuda general o la definicion y ejemplo de una palabra."""
    if palabra is None:
        lineas = ["[OK] Comandos disponibles:"]
        for comando in _COMANDOS_PRINCIPALES:
            definicion = buscar_definicion(comando)
            if definicion is not None:
                lineas.append(
                    f"- {definicion.palabra}: {definicion.definicion} "
                    f"Ejemplo: {definicion.ejemplo}"
                )
        return "\n".join(lineas)

    palabra = palabra.strip()
    definicion = buscar_definicion(palabra)
    if definicion is None:
        return f"[ERROR] No hay ayuda disponible para '{palabra}'."

    return (
        f"[OK] {definicion.palabra} ({definicion.tipo}): "
        f"{definicion.definicion}\n"
        f"Ejemplo: {definicion.ejemplo}"
    )


def mostrar_tokens(texto: str | None = None) -> str:
    """Muestra la tabla de terminales o los tokens de un texto de entrada."""
    if texto is None or not texto.strip():
        lineas = ["[OK] Terminales reconocidos por el lexer:"]
        for definicion in listar_definiciones():
            lineas.append(
                f"{definicion.tipo:<16} {definicion.palabra:<16} "
                f"{definicion.definicion} Ejemplo: {definicion.ejemplo}"
            )
        return "\n".join(lineas)

    reconocidos = tokenizar(texto)
    tiene_error = any(token.tipo == "ERROR" for token in reconocidos)
    prefijo = (
        "[ERROR] Se encontraron caracteres no reconocidos:"
        if tiene_error
        else "[OK] Tokens reconocidos:"
    )
    lineas = [prefijo]
    for token in reconocidos:
        lineas.append(
            f"{token.tipo:<16} {token.lexema!r:<24} "
            f"línea {token.linea}, columna {token.columna}"
        )
    return "\n".join(lineas)


def despachar(orden: Orden) -> str:
    """Resuelve los comandos de ayuda y tokens asignados a esta tarea."""
    comando = orden.comando.lower()
    if comando == "ayuda":
        if len(orden.argumentos) > 1:
            return "[ERROR] Uso: ayuda [comando]."
        palabra = str(orden.argumentos[0]) if orden.argumentos else None
        return ayuda(palabra)

    if comando == "tokens":
        texto = " ".join(str(argumento) for argumento in orden.argumentos)
        return mostrar_tokens(texto)

    return f"[ERROR] Despacho pendiente para el comando '{orden.comando}'."


__all__ = ["ayuda", "despachar", "mostrar_tokens"]
