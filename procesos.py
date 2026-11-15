"""Gestion de procesos del simulador. Stub temporal de T1.3."""

from dataclasses import dataclass
from enum import Enum


class EstadoProceso(str, Enum):
    """Estados del ciclo de vida de un proceso."""

    NUEVO = "NUEVO"
    LISTO = "LISTO"
    EJECUTANDO = "EJECUTANDO"
    TERMINADO = "TERMINADO"
    RECHAZADO = "RECHAZADO"


@dataclass
class Proceso:
    """Proceso registrado por el simulador."""

    pid: int
    nombre: str
    llegada: int
    cpu: int
    prioridad: int
    memoria: int
    estado: EstadoProceso = EstadoProceso.NUEVO


def crear_proceso(
    nombre: str,
    llegada: int = 0,
    cpu: int = 1,
    prioridad: int = 1,
    memoria: int = 64,
) -> Proceso:
    """Devuelve un proceso falso sin registrarlo.

    Stub T1.3: la validacion, el registro y la reserva de memoria se
    implementan en T3.1 y T4.2.
    """
    return Proceso(
        pid=0,
        nombre=nombre,
        llegada=llegada,
        cpu=cpu,
        prioridad=prioridad,
        memoria=memoria,
        estado=EstadoProceso.LISTO,
    )


def listar_procesos() -> list[Proceso]:
    """Devuelve los procesos registrados."""
    return []


def consultar_proceso(pid: int) -> Proceso | None:
    """Devuelve un proceso por su pid, o None si no existe."""
    return None


def finalizar_proceso(pid: int) -> Proceso | None:
    """Finaliza un proceso y lo devuelve, o None si no existe."""
    return None


def cargar_ejemplo() -> list[Proceso]:
    """Carga los cuatro procesos verificados del contrato T1.2."""
    return [
        Proceso(1, "P1", 0, 8, 2, 128, EstadoProceso.LISTO),
        Proceso(2, "P2", 1, 4, 1, 64, EstadoProceso.LISTO),
        Proceso(3, "P3", 2, 9, 3, 256, EstadoProceso.LISTO),
        Proceso(4, "P4", 3, 5, 2, 100, EstadoProceso.LISTO),
    ]
