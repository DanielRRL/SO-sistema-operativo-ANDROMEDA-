"""Gestion de procesos y ciclo de vida del simulador."""

import re
from dataclasses import dataclass
from enum import Enum

from memoria import liberar as liberar_memoria
from memoria import reiniciar_memoria
from memoria import reservar as reservar_memoria
from tokens import RESERVADAS


PATRON_NOMBRE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


class EstadoProceso(str, Enum):
    """Estados del ciclo de vida de un proceso."""

    NUEVO = "NUEVO"
    LISTO = "LISTO"
    EJECUTANDO = "EJECUTANDO"
    TERMINADO = "TERMINADO"
    RECHAZADO = "RECHAZADO"


def _validar_nombre(nombre: str) -> None:
    if not isinstance(nombre, str) or not PATRON_NOMBRE.fullmatch(nombre):
        raise ValueError(
            "El nombre debe empezar con letra o _ y solo contener letras, "
            "digitos y _."
        )
    if nombre.lower() in RESERVADAS:
        raise ValueError("El nombre del proceso no puede ser una palabra reservada.")


def _validar_entero(campo: str, valor: int, minimo: int) -> None:
    if not isinstance(valor, int) or isinstance(valor, bool) or valor < minimo:
        raise ValueError(f"{campo} debe ser un entero mayor o igual que {minimo}.")


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

    def __post_init__(self) -> None:
        _validar_entero("pid", self.pid, 1)
        _validar_nombre(self.nombre)
        _validar_entero("llegada", self.llegada, 0)
        _validar_entero("cpu", self.cpu, 1)
        _validar_entero("prioridad", self.prioridad, 0)
        _validar_entero("memoria", self.memoria, 1)
        if not isinstance(self.estado, EstadoProceso):
            raise ValueError("El estado del proceso no es valido.")


_procesos: dict[int, Proceso] = {}
_siguiente_pid = 1


def _buscar_por_nombre(nombre: str) -> Proceso | None:
    for proceso in _procesos.values():
        if proceso.nombre == nombre:
            return proceso
    return None


def crear_proceso(
    nombre: str,
    llegada: int = 0,
    cpu: int = 1,
    prioridad: int = 1,
    memoria: int = 64,
) -> Proceso:
    """Crea, valida, registra y reserva memoria para un proceso."""
    global _siguiente_pid

    _validar_nombre(nombre)
    _validar_entero("llegada", llegada, 0)
    _validar_entero("cpu", cpu, 1)
    _validar_entero("prioridad", prioridad, 0)
    _validar_entero("memoria", memoria, 1)
    if _buscar_por_nombre(nombre) is not None:
        raise ValueError(f"Ya existe un proceso con el nombre '{nombre}'.")

    pid = _siguiente_pid
    _siguiente_pid += 1
    proceso = Proceso(
        pid=pid,
        nombre=nombre,
        llegada=llegada,
        cpu=cpu,
        prioridad=prioridad,
        memoria=memoria,
        estado=EstadoProceso.NUEVO,
    )
    if reservar_memoria(pid, memoria):
        proceso.estado = EstadoProceso.LISTO
    else:
        proceso.estado = EstadoProceso.RECHAZADO
    _procesos[pid] = proceso
    return proceso


def listar_procesos() -> list[Proceso]:
    """Devuelve los procesos registrados ordenados por pid."""
    return [_procesos[pid] for pid in sorted(_procesos)]


def consultar_proceso(pid: int) -> Proceso | None:
    """Devuelve un proceso por su pid, o None si no existe."""
    return _procesos.get(pid)


def finalizar_proceso(pid: int) -> Proceso | None:
    """Finaliza un proceso y libera su memoria."""
    proceso = _procesos.get(pid)
    if proceso is None:
        return None
    if proceso.estado not in (EstadoProceso.LISTO, EstadoProceso.EJECUTANDO):
        raise ValueError(
            f"El proceso {pid} esta en estado {proceso.estado.value} y no se "
            "puede finalizar."
        )
    proceso.estado = EstadoProceso.TERMINADO
    liberar_memoria(pid)
    return proceso


def cargar_ejemplo() -> list[Proceso]:
    """Reinicia el registro y carga los cuatro procesos verificados de T1.2."""
    reiniciar_procesos()
    return [
        crear_proceso("P1", llegada=0, cpu=8, prioridad=2, memoria=128),
        crear_proceso("P2", llegada=1, cpu=4, prioridad=1, memoria=64),
        crear_proceso("P3", llegada=2, cpu=9, prioridad=3, memoria=256),
        crear_proceso("P4", llegada=3, cpu=5, prioridad=2, memoria=100),
    ]


def reiniciar_procesos() -> None:
    """Vacia el registro, reinicia el contador de pid y libera la memoria."""
    global _siguiente_pid
    _procesos.clear()
    _siguiente_pid = 1
    reiniciar_memoria()
