from tokens import PALABRAS_RESERVADAS, SIMBOLOS, Token


def tokenizar(texto: str):
    """Tokeniza una línea o bloque de texto según la gramática del simulador."""
    tokens = []
    i = 0
    linea = 1
    columna = 1
    longitud = len(texto)

    while i < longitud:
        ch = texto[i]

        if ch in " \t":
            i += 1
            columna += 1
            continue

        if ch == "\n":
            i += 1
            linea += 1
            columna = 1
            continue

        if ch == "#":
            while i < longitud and texto[i] != "\n":
                i += 1
            continue

        if ch.isalpha() or ch == "_":
            inicio = i
            inicio_columna = columna
            i += 1
            columna += 1

            while i < longitud and (texto[i].isalnum() or texto[i] in "_."):
                i += 1
                columna += 1

            palabra = texto[inicio:i]
            tipo = PALABRAS_RESERVADAS.get(palabra.lower(), "ID")
            tokens.append(Token(tipo, palabra, linea, inicio_columna))
            continue

        if ch.isdigit():
            inicio = i
            inicio_columna = columna
            i += 1
            columna += 1

            while i < longitud and texto[i].isdigit():
                i += 1
                columna += 1

            tokens.append(Token("NUMERO", texto[inicio:i], linea, inicio_columna))
            continue

        if ch == '"':
            inicio_columna = columna
            i += 1
            columna += 1
            valor = []

            while i < longitud:
                caracter = texto[i]
                if caracter == '"':
                    i += 1
                    columna += 1
                    break

                if caracter == "\\":
                    if i + 1 >= longitud:
                        raise ValueError(f"[ERROR] Cadena sin cierre en línea {linea}, columna {inicio_columna}.")
                    escape = texto[i + 1]
                    if escape in {'"', "\\", "n", "t"}:
                        valor.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(escape, escape))
                        i += 2
                        columna += 2
                        continue
                    raise ValueError(f"[ERROR] Secuencia de escape inválida en línea {linea}, columna {columna}.")

                if caracter == "\n":
                    raise ValueError(f"[ERROR] Cadena no cerrada en línea {linea}, columna {inicio_columna}.")

                valor.append(caracter)
                i += 1
                columna += 1
            else:
                raise ValueError(f"[ERROR] Cadena sin cierre en línea {linea}, columna {inicio_columna}.")

            tokens.append(Token("CADENA", "".join(valor), linea, inicio_columna))
            continue

        if ch in SIMBOLOS:
            tokens.append(Token(SIMBOLOS[ch], ch, linea, columna))
            i += 1
            columna += 1
            continue

        raise ValueError(f"[ERROR] Carácter no reconocido '{ch}' en línea {linea}, columna {columna}.")

    return tokens


__all__ = ["tokenizar"]
