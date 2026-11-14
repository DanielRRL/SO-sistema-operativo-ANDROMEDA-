"""Gestion de memoria simulada. Stub temporal de T1.3."""

from dataclasses import dataclass, field


CAPACIDAD_TOTAL = 1024


@dataclass(frozen=True)
class EstadoMemoria:
    """Estado actual de la memoria simulada."""

    total: int
    usada: int
    libre: int
    asignaciones: dict[int, int] = field(default_factory=dict)


def reservar(pid: int, cantidad: int) -> bool:
    """Simula una reserva exitosa.

    Stub T1.3: la validacion real de capacidad corresponde a T3.7.
    """
    return True


def liberar(pid: int) -> int:
    """Simula la liberacion de memoria de un proceso."""
    return 0


def estado_memoria() -> EstadoMemoria:
    """Devuelve la memoria totalmente libre."""
    return EstadoMemoria(
        total=CAPACIDAD_TOTAL,
        usada=0,
        libre=CAPACIDAD_TOTAL,
        asignaciones={},
    )


def reiniciar_memoria() -> None:
    """Deja la memoria como al inicio."""
    return None
