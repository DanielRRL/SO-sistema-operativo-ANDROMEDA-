"""Analizador léxico del simulador."""

import re
from dataclasses import dataclass

from tokens import RESERVADAS, SIMBOLOS


@dataclass(frozen=True)
class Token:
    """Token reconocido por el lexer."""

    tipo: str
    lexema: str
    linea: int
    columna: int


PATRON_ARCHIVO = re.compile(r"[A-Za-z0-9_\-]+\.[A-Za-z0-9]+")
ESCAPES = {'"': '"', "\\": "\\", "n": "\n", "t": "\t"}


def _es_letra(caracter: str) -> bool:
    return caracter == "_" or "A" <= caracter <= "Z" or "a" <= caracter <= "z"


def _es_digito(caracter: str) -> bool:
    return "0" <= caracter <= "9"


def _es_alnum(caracter: str) -> bool:
    return _es_letra(caracter) or _es_digito(caracter)


def tokenizar(texto: str) -> list[Token]:
    """Convierte una línea o bloque de texto en tokens terminados en FIN.

    Reconoce palabras reservadas, identificadores, nombres de archivo, números,
    cadenas, el símbolo igual y comentarios. Los caracteres inválidos y las
    cadenas sin cerrar generan un token ERROR y el análisis continúa.
    """
    tokens: list[Token] = []
    i = 0
    linea = 1
    columna = 1
    longitud = len(texto)

    while i < longitud:
        caracter = texto[i]

        if caracter in " \t\r":
            i += 1
            columna += 1
            continue

        if caracter == "\n":
            i += 1
            linea += 1
            columna = 1
            continue

        if caracter == "#":
            while i < longitud and texto[i] != "\n":
                i += 1
                columna += 1
            continue

        archivo = PATRON_ARCHIVO.match(texto, i)
        if archivo:
            lexema = archivo.group(0)
            tokens.append(Token("NOMBRE_ARCHIVO", lexema, linea, columna))
            i += len(lexema)
            columna += len(lexema)
            continue

        if _es_letra(caracter):
            inicio = i
            inicio_columna = columna
            i += 1
            columna += 1
            while i < longitud and _es_alnum(texto[i]):
                i += 1
                columna += 1
            lexema = texto[inicio:i]
            tipo = RESERVADAS.get(lexema.lower(), "ID")
            tokens.append(Token(tipo, lexema, linea, inicio_columna))
            continue

        if _es_digito(caracter):
            inicio = i
            inicio_columna = columna
            i += 1
            columna += 1
            while i < longitud and _es_digito(texto[i]):
                i += 1
                columna += 1
            tokens.append(Token("NUMERO", texto[inicio:i], linea, inicio_columna))
            continue

        if caracter == '"':
            inicio = i
            inicio_linea = linea
            inicio_columna = columna
            i += 1
            columna += 1
            valor: list[str] = []
            cerrada = False

            while i < longitud:
                actual = texto[i]
                if actual == '"':
                    i += 1
                    columna += 1
                    cerrada = True
                    break
                if actual == "\n":
                    break
                if actual == "\\":
                    if i + 1 >= longitud or texto[i + 1] == "\n":
                        break
                    escape = texto[i + 1]
                    if escape in ESCAPES:
                        valor.append(ESCAPES[escape])
                    else:
                        valor.extend(["\\", escape])
                    i += 2
                    columna += 2
                    continue
                valor.append(actual)
                i += 1
                columna += 1

            if not cerrada:
                tokens.append(Token("ERROR", texto[inicio:i], inicio_linea, inicio_columna))
                continue
            tokens.append(Token("CADENA", "".join(valor), inicio_linea, inicio_columna))
            continue

        if caracter in SIMBOLOS:
            tokens.append(Token(SIMBOLOS[caracter], caracter, linea, columna))
            i += 1
            columna += 1
            continue

        tokens.append(Token("ERROR", caracter, linea, columna))
        i += 1
        columna += 1

    tokens.append(Token("FIN", "", linea, columna))
    return tokens


__all__ = ["Token", "tokenizar"]
