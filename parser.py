"""parser.py - Parser de ordenes del simulador (T3.9).

Recibe los tokens del lexer, valida que cumplan la gramatica y arma una Orden
para el despachador. Si algo esta mal lanza ErrorSintaxis (que es un
ValueError, como pide docs/firmas_modulos.md) con el mensaje y el uso correcto.

Sintaxis (referencia de docs/firmas_modulos.md, seccion 1.1):
    crear proceso <nombre> cpu=<n> [llegada=<n>] [prioridad=<n>] [mem=<n>]
    listar procesos | consultar proceso <pid> | finalizar proceso <pid>
    planificar fcfs | sjf | rr [quantum=<n>]
    estadisticas | ejemplo | limpiar | salir
    concurrencia sin_lock | con_lock | semaforo
    mensaje enviar "<texto>" | mensaje recibir
    memoria [estado] | memoria asignar <pid> <mb> | memoria liberar <pid>
    archivo crear|modificar|leer|eliminar|listar ...
    ayuda [palabra] | tokens <cualquier cosa>
"""

from dataclasses import dataclass, field, replace

from lexer import Token

QUANTUM_POR_DEFECTO = 3

# Las 36 palabras reservadas del lenguaje. Se usan para reconocer palabras clave
# y para rechazar nombres de proceso que coincidan con ellas.
PALABRAS_RESERVADAS = frozenset("""
    crear listar consultar finalizar planificar estadisticas concurrencia mensaje
    memoria archivo ejemplo ayuda tokens limpiar salir proceso procesos asignar
    liberar estado enviar recibir leer modificar eliminar fcfs sjf rr sin_lock
    con_lock semaforo llegada cpu prioridad mem quantum
""".split())

ATRIBUTOS = ("llegada", "cpu", "prioridad", "mem")

USO = {
    "crear": "crear proceso <nombre> cpu=<n> [llegada=<n>] [prioridad=<n>] [mem=<n>]",
    "listar": "listar procesos",
    "consultar": "consultar proceso <pid>",
    "finalizar": "finalizar proceso <pid>",
    "planificar": "planificar fcfs | planificar sjf | planificar rr [quantum=<n>]",
    "estadisticas": "estadisticas",
    "concurrencia": "concurrencia sin_lock | concurrencia con_lock | concurrencia semaforo",
    "mensaje": 'mensaje enviar "<texto>" | mensaje recibir',
    "memoria": "memoria estado | memoria asignar <pid> <mb> | memoria liberar <pid>",
    "archivo": ('archivo crear <nombre.ext> ["<texto>"] | archivo listar | archivo leer <nombre.ext> '
                '| archivo modificar <nombre.ext> "<texto>" | archivo eliminar <nombre.ext>'),
    "ayuda": "ayuda [palabra]",
    "ejemplo": "ejemplo",
    "limpiar": "limpiar",
    "salir": "salir",
}


class ErrorSintaxis(ValueError):
    """La linea no cumple la gramatica. El mensaje ya incluye el uso correcto."""


@dataclass(frozen=True)
class Orden:
    """Orden estructurada que recibe el despachador."""

    comando: str
    subcomando: str | None = None
    argumentos: tuple[str | int, ...] = ()
    atributos: dict[str, int] = field(default_factory=dict)
    linea_original: str = ""


# ----------------------------------------------------------------- utilidades
def _palabra(tok: Token | None) -> str | None:
    """Devuelve la palabra reservada (en minuscula) que es el token, o None.

    Compara por el texto, asi funciona aunque tokens.py clasifique la palabra
    con otro tipo de token (o como ID).
    """
    if tok is None or tok.tipo in ("CADENA", "NUMERO", "NOMBRE_ARCHIVO", "IGUAL", "ERROR", "FIN"):
        return None
    minuscula = tok.lexema.lower()
    if tok.tipo != "ID" or minuscula in PALABRAS_RESERVADAS:
        return minuscula
    return None


def _texto(tok: Token) -> str:
    """Texto del token tal como lo escribio el usuario (las cadenas con comillas)."""
    return f'"{tok.lexema}"' if tok.tipo == "CADENA" else tok.lexema


def _unir(tokens: list[Token]) -> str:
    """Reconstruye la linea con espacios, pero sin espacios alrededor de '='."""
    texto = ""
    for tok in tokens:
        if tok.tipo == "IGUAL" or texto.endswith("="):
            texto += _texto(tok)
        else:
            texto += (" " if texto else "") + _texto(tok)
    return texto


def _encontrado(tok: Token | None) -> str:
    if tok is None:
        return " pero la linea termina ahi"
    return f" pero se encontro '{_texto(tok)}' en la columna {tok.columna}"


def _error(mensaje: str, comando: str | None = None) -> ErrorSintaxis:
    if comando in USO:
        mensaje += "\nUso: " + USO[comando]
    return ErrorSintaxis(mensaje)


class _Cursor:
    """Recorre los tokens (sin el FIN) de izquierda a derecha."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def actual(self) -> Token | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def avanzar(self) -> Token | None:
        tok = self.actual()
        self.pos += 1
        return tok

    def quedan(self) -> bool:
        return self.pos < len(self.tokens)


def _exigir(cur: _Cursor, comando: str, *validas: str) -> str:
    """Exige que el siguiente token sea una de las palabras validas."""
    tok = cur.actual()
    palabra = _palabra(tok)
    if palabra not in validas:
        opciones = " o ".join(f"'{v}'" for v in validas)
        raise _error(f"se esperaba {opciones}" + _encontrado(tok), comando)
    cur.avanzar()
    return palabra


def _numero(cur: _Cursor, comando: str, que: str) -> int:
    tok = cur.actual()
    if tok is None or tok.tipo != "NUMERO":
        raise _error(f"se esperaba un numero para {que}" + _encontrado(tok), comando)
    cur.avanzar()
    return int(tok.lexema)


def _cadena(cur: _Cursor, comando: str) -> str:
    tok = cur.actual()
    if tok is None or tok.tipo != "CADENA":
        raise _error('se esperaba un texto entre comillas, por ejemplo "hola"' + _encontrado(tok), comando)
    cur.avanzar()
    return tok.lexema


def _nombre_archivo(cur: _Cursor, comando: str) -> str:
    tok = cur.actual()
    if tok is None or tok.tipo != "NOMBRE_ARCHIVO":
        raise _error("se esperaba un nombre de archivo con extension (por ejemplo notas.txt)"
                     + _encontrado(tok), comando)
    cur.avanzar()
    return tok.lexema


def _fin(cur: _Cursor, comando: str) -> None:
    """Exige que no sobre nada al final de la linea."""
    tok = cur.actual()
    if tok is not None:
        raise _error(f"sobra '{_texto(tok)}' en la columna {tok.columna}", comando)


# ------------------------------------------------------------------- comandos
def _crear(cur: _Cursor) -> Orden:
    _exigir(cur, "crear", "proceso")
    tok = cur.avanzar()
    if tok is None:
        raise _error("falta el nombre del proceso", "crear")
    if _palabra(tok) is not None:
        raise _error(f"'{tok.lexema}' es una palabra reservada; elige otro nombre para el proceso", "crear")
    if tok.tipo != "ID":
        raise _error(f"nombre de proceso invalido '{_texto(tok)}' (use letras, digitos y _; no empiece con digito)", "crear")
    nombre = tok.lexema

    atributos: dict[str, int] = {}
    while cur.quedan():
        tok = cur.avanzar()
        clave = _palabra(tok)
        if clave not in ATRIBUTOS:
            raise _error("se esperaba un atributo (llegada, cpu, prioridad o mem)"
                         f" pero se encontro '{_texto(tok)}' en la columna {tok.columna}", "crear")
        destino = "memoria" if clave == "mem" else clave      # nombre del parametro de crear_proceso
        if destino in atributos:
            raise _error(f"el atributo '{clave}' esta repetido (columna {tok.columna})", "crear")
        igual = cur.actual()
        if igual is None or igual.tipo != "IGUAL":
            raise _error(f"falta '=' despues de '{clave}'" + _encontrado(igual), "crear")
        cur.avanzar()
        atributos[destino] = _numero(cur, "crear", f"{clave}=")

    if "cpu" not in atributos:
        raise _error("falta el atributo cpu=<n>", "crear")
    if atributos["cpu"] < 1:
        raise _error("cpu debe ser al menos 1", "crear")
    if atributos.get("memoria", 1) < 1:
        raise _error("mem debe ser al menos 1", "crear")
    return Orden("crear", "proceso", (nombre,), atributos)


def _listar(cur: _Cursor) -> Orden:
    _exigir(cur, "listar", "procesos")
    _fin(cur, "listar")
    return Orden("listar", "procesos")


def _consultar(cur: _Cursor) -> Orden:
    _exigir(cur, "consultar", "proceso")
    pid = _numero(cur, "consultar", "el pid")
    _fin(cur, "consultar")
    return Orden("consultar", "proceso", (pid,))


def _finalizar(cur: _Cursor) -> Orden:
    _exigir(cur, "finalizar", "proceso")
    pid = _numero(cur, "finalizar", "el pid")
    _fin(cur, "finalizar")
    return Orden("finalizar", "proceso", (pid,))


def _planificar(cur: _Cursor) -> Orden:
    algoritmo = _exigir(cur, "planificar", "fcfs", "sjf", "rr")
    atributos: dict[str, int] = {}
    if algoritmo == "rr":
        quantum = QUANTUM_POR_DEFECTO
        if cur.quedan():
            _exigir(cur, "planificar", "quantum")
            igual = cur.actual()
            if igual is None or igual.tipo != "IGUAL":
                raise _error("falta '=' despues de 'quantum'" + _encontrado(igual), "planificar")
            cur.avanzar()
            quantum = _numero(cur, "planificar", "quantum=")
            if quantum < 1:
                raise _error("el quantum debe ser al menos 1", "planificar")
        atributos["quantum"] = quantum
    _fin(cur, "planificar")
    return Orden("planificar", algoritmo, (), atributos)


def _concurrencia(cur: _Cursor) -> Orden:
    modo = _exigir(cur, "concurrencia", "sin_lock", "con_lock", "semaforo")
    _fin(cur, "concurrencia")
    return Orden("concurrencia", modo)


def _mensaje(cur: _Cursor) -> Orden:
    accion = _exigir(cur, "mensaje", "enviar", "recibir")
    argumentos: tuple = ()
    if accion == "enviar":
        argumentos = (_cadena(cur, "mensaje"),)
    _fin(cur, "mensaje")
    return Orden("mensaje", accion, argumentos)


def _memoria(cur: _Cursor) -> Orden:
    if not cur.quedan():                       # 'memoria' solo equivale a 'memoria estado'
        return Orden("memoria", "estado")
    accion = _exigir(cur, "memoria", "estado", "asignar", "liberar")
    argumentos: tuple = ()
    if accion == "asignar":
        pid = _numero(cur, "memoria", "el pid")
        mb = _numero(cur, "memoria", "los MB")
        if mb < 1:
            raise _error("los MB a asignar deben ser al menos 1", "memoria")
        argumentos = (pid, mb)
    elif accion == "liberar":
        argumentos = (_numero(cur, "memoria", "el pid"),)
    _fin(cur, "memoria")
    return Orden("memoria", accion, argumentos)


def _archivo(cur: _Cursor) -> Orden:
    accion = _exigir(cur, "archivo", "crear", "listar", "leer", "modificar", "eliminar")
    argumentos: tuple = ()
    if accion == "crear":
        nombre = _nombre_archivo(cur, "archivo")
        texto = _cadena(cur, "archivo") if cur.quedan() else ""
        argumentos = (nombre, texto)
    elif accion == "modificar":
        nombre = _nombre_archivo(cur, "archivo")
        argumentos = (nombre, _cadena(cur, "archivo"))
    elif accion in ("leer", "eliminar"):
        argumentos = (_nombre_archivo(cur, "archivo"),)
    _fin(cur, "archivo")
    return Orden("archivo", accion, argumentos)


def _ayuda(cur: _Cursor) -> Orden:
    argumentos: tuple = ()
    if cur.quedan():
        tok = cur.avanzar()
        if tok.tipo != "ID" and _palabra(tok) is None:
            raise _error(f"se esperaba una palabra, por ejemplo 'ayuda planificar', pero se encontro '{_texto(tok)}'", "ayuda")
        argumentos = (tok.lexema.lower(),)
    _fin(cur, "ayuda")
    return Orden("ayuda", None, argumentos)


def _sin_argumentos(nombre: str):
    def manejador(cur: _Cursor) -> Orden:
        _fin(cur, nombre)
        return Orden(nombre)
    return manejador


COMANDOS = {
    "crear": _crear, "listar": _listar, "consultar": _consultar, "finalizar": _finalizar,
    "planificar": _planificar, "concurrencia": _concurrencia, "mensaje": _mensaje,
    "memoria": _memoria, "archivo": _archivo, "ayuda": _ayuda,
    "estadisticas": _sin_argumentos("estadisticas"), "ejemplo": _sin_argumentos("ejemplo"),
    "limpiar": _sin_argumentos("limpiar"), "salir": _sin_argumentos("salir"),
}


# ----------------------------------------------------------------- principal
def parsear(tokens: list[Token]) -> Orden:
    """Valida los tokens y devuelve la Orden. Lanza ErrorSintaxis si hay un error."""
    utiles = [t for t in tokens if t.tipo != "FIN"]
    linea = _unir(utiles)
    if not utiles:
        return Orden(comando="")

    # 'tokens' es una herramienta de depuracion: acepta cualquier cosa despues
    # (incluso tokens ERROR) porque justamente sirve para verlos.
    if _palabra(utiles[0]) == "tokens":
        return Orden("tokens", linea_original=linea)

    for tok in utiles:
        if tok.tipo == "ERROR":
            if tok.lexema.startswith('"'):
                raise ErrorSintaxis(f"comilla sin cerrar en la columna {tok.columna}")
            raise ErrorSintaxis(f"caracter no reconocido '{tok.lexema}' en la columna {tok.columna}")

    cur = _Cursor(utiles)
    primero = cur.avanzar()
    comando = _palabra(primero)
    if comando is None:
        raise ErrorSintaxis(f"comando desconocido '{_texto(primero)}'. Escribe 'ayuda' para ver los comandos.")
    manejador = COMANDOS.get(comando)
    if manejador is None:
        raise ErrorSintaxis(f"'{primero.lexema}' no es un comando. Escribe 'ayuda' para ver los comandos.")
    return replace(manejador(cur), linea_original=linea)