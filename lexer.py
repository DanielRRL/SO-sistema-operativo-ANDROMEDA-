"""Analizador lexico del simulador. Stub temporal de T1.3."""

from dataclasses import dataclass

from tokens import RESERVADAS


@dataclass(frozen=True)
class Token:
    """Token reconocido por el lexer."""

    tipo: str
    lexema: str
    columna: int


def tokenizar(linea: str) -> list[Token]:
    """Convierte una linea en una lista de tokens terminada en FIN.

    Stub T1.3: separa por espacios y consulta las palabras reservadas si ya
    existen. Se reemplaza por el lexer real en T3.5.
    """
    tokens: list[Token] = []
    columna = 0
    for palabra in linea.split():
        columna = linea.index(palabra, columna)
        tipo = RESERVADAS.get(palabra.lower(), "PALABRA")
        tokens.append(Token(tipo, palabra, columna + 1))
        columna += len(palabra)
    tokens.append(Token("FIN", "", len(linea) + 1))
    return tokens
