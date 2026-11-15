"""Operaciones de archivos dentro de carpeta_pruebas. Stub temporal de T1.3."""

from dataclasses import dataclass
from pathlib import Path


CARPETA_PRUEBAS = Path("carpeta_pruebas")


@dataclass(frozen=True)
class ArchivoInfo:
    """Informacion basica de un archivo del simulador."""

    nombre: str
    tamano: int


def validar_nombre(nombre: str) -> str:
    """Devuelve el nombre sin validar rutas todavia.

    Stub T1.3: la validacion de seguridad corresponde a T3.8.
    """
    return nombre


def crear_archivo(nombre: str, contenido: str = "") -> ArchivoInfo:
    """Devuelve la informacion de un archivo falso."""
    return ArchivoInfo(nombre=nombre, tamano=len(contenido))


def listar_archivos() -> list[ArchivoInfo]:
    """Devuelve una lista vacia de archivos."""
    return []


def leer_archivo(nombre: str) -> str:
    """Devuelve el contenido vacio de un archivo falso."""
    return ""


def modificar_archivo(nombre: str, contenido: str) -> ArchivoInfo:
    """Devuelve la informacion de un archivo falso modificado."""
    return ArchivoInfo(nombre=nombre, tamano=len(contenido))


def eliminar_archivo(nombre: str) -> bool:
    """Simula la eliminacion exitosa de un archivo."""
    return True


def existe_archivo(nombre: str) -> bool:
    """Indica que el archivo no existe en el stub."""
    return False
