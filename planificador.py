"""Planificadores FCFS, SJF y Round Robin. Stubs temporales de T1.3."""

from dataclasses import dataclass

from procesos import Proceso


@dataclass(frozen=True)
class Ejecucion:
    """Segmento continuo de CPU para el Gantt."""

    pid: int
    nombre: str
    inicio: int
    fin: int


@dataclass(frozen=True)
class TiempoProceso:
    """Tiempos calculados para un proceso planificado."""

    pid: int
    nombre: str
    llegada: int
    cpu: int
    inicio: int
    fin: int
    retorno: int
    espera: int


@dataclass(frozen=True)
class ResultadoPlanificacion:
    """Resultado completo de una planificacion."""

    algoritmo: str
    quantum: int | None
    ejecuciones: list[Ejecucion]
    tiempos: list[TiempoProceso]
    promedio_retorno: float
    promedio_espera: float


def _resultado_vacio(
    algoritmo: str,
    quantum: int | None = None,
) -> ResultadoPlanificacion:
    return ResultadoPlanificacion(
        algoritmo=algoritmo,
        quantum=quantum,
        ejecuciones=[],
        tiempos=[],
        promedio_retorno=0.0,
        promedio_espera=0.0,
    )


def fcfs(procesos: list[Proceso]) -> ResultadoPlanificacion:
    """Devuelve un resultado FCFS vacio.

    Stub T1.3: la implementacion real corresponde a T3.2.
    """
    return _resultado_vacio("FCFS")


def sjf(procesos: list[Proceso]) -> ResultadoPlanificacion:
    """Devuelve un resultado SJF vacio.

    Stub T1.3: la implementacion real corresponde a T3.2.
    """
    return _resultado_vacio("SJF")


def rr(
    procesos: list[Proceso],
    quantum: int = 3,
) -> ResultadoPlanificacion:
    """Devuelve un resultado Round Robin vacio.

    Stub T1.3: la implementacion real corresponde a T3.3.
    """
    if quantum < 1:
        raise ValueError("El quantum debe ser mayor o igual que 1")
    return _resultado_vacio("RR", quantum)


def planificar(
    procesos: list[Proceso],
    algoritmo: str,
    quantum: int = 3,
) -> ResultadoPlanificacion:
    """Despacha la planificacion al algoritmo indicado."""
    nombre = algoritmo.upper()
    if nombre == "FCFS":
        return fcfs(procesos)
    if nombre == "SJF":
        return sjf(procesos)
    if nombre == "RR":
        return rr(procesos, quantum)
    raise ValueError(f"Algoritmo de planificacion no reconocido: {algoritmo}")
