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


PALABRAS: tuple[str, ...] = ()
RESERVADAS: dict[str, str] = {palabra: palabra.upper() for palabra in PALABRAS}
TERMINALES: dict[str, DefinicionToken] = {}


def buscar_definicion(palabra: str) -> DefinicionToken | None:
    """Devuelve la definicion de una palabra, o None si no existe."""
    return TERMINALES.get(palabra.lower())


def listar_definiciones() -> list[DefinicionToken]:
    """Devuelve todas las definiciones registradas."""
    return list(TERMINALES.values())
