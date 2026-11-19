"""main.py - Punto de entrada del simulador de SO (consola de comandos)."""

import os
import sys

from consola import despachar, mostrar_tokens
from lexer import tokenizar
from parser import ErrorSintaxis, parsear

PROMPT = "simulador> "


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def ejecutar_linea(linea):
    """Procesa una linea. Devuelve False si hay que terminar el programa."""
    linea = linea.strip()
    if not linea:
        return True

    try:
        orden = parsear(tokenizar(linea))
    except ErrorSintaxis as error:
        print(f"[ERROR] {error}")
        return True

    if orden.comando == "":
        return True
    if orden.comando == "salir":
        print("[OK] Hasta luego.")
        return False
    if orden.comando == "limpiar":
        limpiar_pantalla()
        return True
    if orden.comando == "tokens":
        texto = linea[len("tokens"):].strip()
        print(mostrar_tokens(texto or None))
        return True
    if orden.comando == "ayuda":
        print(despachar(orden))
        return True

    print(orden)
    return True


def ejecutar_script(ruta):
    """Ejecuta los comandos de un archivo, uno por linea."""
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:
            lineas = archivo.readlines()
    except OSError as error:
        print(f"[ERROR] No se pudo abrir el script '{ruta}': {error.strerror}")
        return

    for linea in lineas:
        texto = linea.strip()
        if not texto or texto.startswith("#"):
            continue
        print(PROMPT + texto)
        if not ejecutar_linea(texto):
            break


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--script":
        if len(sys.argv) < 3:
            print("[ERROR] Uso: python main.py --script archivo")
        else:
            ejecutar_script(sys.argv[2])
        return

    print("Simulador de Sistema Operativo. Escribe 'salir' para terminar.")
    while True:
        try:
            linea = input(PROMPT)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\n[AVISO] Usa 'salir' para terminar.")
            continue
        if not ejecutar_linea(linea):
            break


if __name__ == "__main__":
    main()
