"""Operaciones seguras de archivos dentro de carpeta_pruebas."""

import re
from dataclasses import dataclass
from pathlib import Path
from pathlib import PureWindowsPath

from tokens import PALABRAS_RESERVADAS


CARPETA_PRUEBAS = Path("carpeta_pruebas")
_PATRON_NOMBRE = re.compile(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*\Z")


@dataclass(frozen=True)
class ArchivoInfo:
    """Informacion basica de un archivo del simulador."""

    nombre: str
    tamano: int


def validar_nombre(nombre: str) -> str:
    """Valida que el nombre sea un archivo simple, no una ruta."""
    if not isinstance(nombre, str) or not nombre:
        raise ValueError("El nombre del archivo no puede estar vacio.")
    if (
        Path(nombre).is_absolute()
        or PureWindowsPath(nombre).is_absolute()
        or "/" in nombre
        or "\\" in nombre
        or ".." in nombre
        or not _PATRON_NOMBRE.fullmatch(nombre)
    ):
        raise ValueError("El nombre debe ser un archivo simple dentro de carpeta_pruebas.")

    nombre_base = nombre.rsplit(".", 1)[0].lower()
    if nombre_base in PALABRAS_RESERVADAS:
        raise ValueError("El nombre del archivo no puede ser una palabra reservada.")

    return nombre


def _ruta_archivo(nombre: str) -> Path:
    """Obtiene la ruta validada, rechazando enlaces que salgan de la carpeta."""
    nombre_validado = validar_nombre(nombre)
    raiz = _raiz_pruebas()
    ruta = raiz / nombre_validado
    ruta_resuelta = ruta.resolve()
    if ruta_resuelta != ruta:
        raise ValueError("La ruta del archivo no puede salir de carpeta_pruebas ni usar enlaces.")
    return ruta


def _raiz_pruebas() -> Path:
    """Crea y valida la carpeta de pruebas, sin seguir un enlace de directorio."""
    raiz_configurada = CARPETA_PRUEBAS.absolute()
    raiz_configurada.mkdir(parents=True, exist_ok=True)
    raiz = raiz_configurada.resolve()
    if raiz != raiz_configurada:
        raise ValueError("carpeta_pruebas no puede ser un enlace a otra ubicacion.")
    return raiz


def _informacion(ruta: Path) -> ArchivoInfo:
    return ArchivoInfo(nombre=ruta.name, tamano=ruta.stat().st_size)


def crear_archivo(nombre: str, contenido: str = "") -> ArchivoInfo:
    """Crea un archivo nuevo sin sobrescribir uno existente."""
    ruta = _ruta_archivo(nombre)
    with ruta.open("x", encoding="utf-8", newline="") as archivo:
        archivo.write(contenido)
    return _informacion(ruta)


def listar_archivos() -> list[ArchivoInfo]:
    """Devuelve los archivos regulares disponibles en carpeta_pruebas."""
    raiz = _raiz_pruebas()
    archivos = []
    for ruta in sorted(raiz.iterdir(), key=lambda item: item.name.lower()):
        if not ruta.is_symlink() and ruta.is_file():
            archivos.append(_informacion(ruta))
    return archivos


def leer_archivo(nombre: str) -> str:
    """Lee el contenido de un archivo validado."""
    ruta = _ruta_archivo(nombre)
    with ruta.open("r", encoding="utf-8", newline="") as archivo:
        return archivo.read()


def modificar_archivo(nombre: str, contenido: str) -> ArchivoInfo:
    """Agrega contenido al final de un archivo existente."""
    ruta = _ruta_archivo(nombre)
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe el archivo '{nombre}'.")
    with ruta.open("a", encoding="utf-8", newline="") as archivo:
        archivo.write(contenido)
    return _informacion(ruta)


def eliminar_archivo(nombre: str) -> bool:
    """Elimina un archivo; devuelve False si no existe."""
    ruta = _ruta_archivo(nombre)
    try:
        ruta.unlink()
    except FileNotFoundError:
        return False
    return True


def existe_archivo(nombre: str) -> bool:
    """Indica si existe un archivo regular dentro de carpeta_pruebas."""
    ruta = _ruta_archivo(nombre)
    return ruta.is_file()
