"""Gestion de memoria simulada del sistema operativo."""

from dataclasses import dataclass, field


CAPACIDAD_TOTAL = 1024
_asignaciones: dict[int, int] = {}


@dataclass(frozen=True)
class EstadoMemoria:
    """Estado actual de la memoria simulada."""

    total: int
    usada: int
    libre: int
    asignaciones: dict[int, int] = field(default_factory=dict)


def reservar(pid: int, cantidad: int) -> bool:
    """Reserva memoria para un proceso si hay capacidad disponible."""
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 0:
        raise ValueError("El pid debe ser un entero positivo.")
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
        raise ValueError("La cantidad de memoria debe ser un entero positivo.")
    if pid in _asignaciones:
        return False

    usada = sum(_asignaciones.values())
    if cantidad > CAPACIDAD_TOTAL - usada:
        return False

    _asignaciones[pid] = cantidad
    return True


def liberar(pid: int) -> int:
    """Libera la memoria de un proceso y devuelve los MB liberados."""
    return _asignaciones.pop(pid, 0)


def estado_memoria() -> EstadoMemoria:
    """Devuelve una fotografia del uso y las asignaciones actuales."""
    asignaciones = _asignaciones.copy()
    usada = sum(asignaciones.values())
    return EstadoMemoria(
        total=CAPACIDAD_TOTAL,
        usada=usada,
        libre=CAPACIDAD_TOTAL - usada,
        asignaciones=asignaciones,
    )


def reiniciar_memoria() -> None:
    """Deja la memoria simulada como al inicio."""
    _asignaciones.clear()
