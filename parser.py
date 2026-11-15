"""Parser de ordenes del simulador. Stub temporal de T1.3."""

from dataclasses import dataclass, field

from lexer import Token


@dataclass(frozen=True)
class Orden:
    """Orden estructurada que recibe el despachador."""

    comando: str
    subcomando: str | None = None
    argumentos: tuple[str | int, ...] = ()
    atributos: dict[str, int] = field(default_factory=dict)
    linea_original: str = ""


def parsear(tokens: list[Token]) -> Orden:
    """Construye una orden a partir de los tokens.

    Stub T1.3: usa el primer token como comando y el resto como argumentos.
    La validacion completa de la gramatica corresponde a T3.9.
    """
    utiles = [token for token in tokens if token.tipo != "FIN"]
    if not utiles:
        return Orden(comando="")
    comando = utiles[0].lexema.lower()
    argumentos = tuple(token.lexema for token in utiles[1:])
    linea_original = " ".join(token.lexema for token in utiles)
    return Orden(
        comando=comando,
        argumentos=argumentos,
        linea_original=linea_original,
    )
