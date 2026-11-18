# Este es el archivo
"""main.py - Punto de entrada del simulador de SO (consola de comandos).

Esqueleto (T2.1): mantiene el bucle de entrada. T3.6 conecta temporalmente
los comandos ayuda y tokens; los demas se integran en T4.1.
"""
import os

PROMPT = "simulador> "

# --- Lexer: usa el real de B si ya existe; si no, uno falso para poder avanzar ---
try:
    from lexer import tokenizar          # lexer.py de la persona B
except ImportError:
    from dataclasses import dataclass

    @dataclass
    class Token:
        tipo: str
        lexema: str
        columna: int

    def tokenizar(linea):
        """Lexer FALSO: cada palabra separada por espacios es un token."""
        tokens, col = [], 0
        for palabra in linea.split():
            col = linea.index(palabra, col)
            tokens.append(Token("PALABRA", palabra, col + 1))
            col += len(palabra)
        tokens.append(Token("FIN", "", len(linea) + 1))
        return tokens


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_tokens(tokens):
    for t in tokens:
        if t.tipo != "FIN":
            print(f"{t.tipo:<14}{t.lexema!r:<14}col {t.columna}")
    print("FIN")


def ejecutar_linea(linea):
    """Procesa una linea. Devuelve False si hay que terminar el programa."""
    linea = linea.strip()
    if not linea:                         # linea vacia: no hace nada
        return True

    primera = linea.split()[0].lower()
    if primera == "salir":
        print("[OK] Hasta luego.")
        return False
    if primera == "limpiar":
        limpiar_pantalla()
        return True

    if primera in {"ayuda", "tokens"}:
        from consola import despachar
        from parser import parsear

        try:
            print(despachar(parsear(tokenizar(linea))))
        except ValueError as error:
            print(f"[ERROR] {error}")
        return True

    # TODO (T3.9 y T4.1): conectar los demas comandos con parser y despachador.
    mostrar_tokens(tokenizar(linea))
    return True


def main():
    print("Simulador de Sistema Operativo. Escribe 'salir' para terminar.")
    while True:
        try:
            linea = input(PROMPT)
        except EOFError:                  # Ctrl+D / fin de entrada
            print()
            break
        except KeyboardInterrupt:         # Ctrl+C: no se cae, avisa
            print("\n[AVISO] Usa 'salir' para terminar.")
            continue
        if not ejecutar_linea(linea):
            break


if __name__ == "__main__":
    main()