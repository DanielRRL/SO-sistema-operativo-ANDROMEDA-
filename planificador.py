"""Planificadores FCFS, SJF y Round Robin del simulador."""

from collections import deque
from dataclasses import dataclass

from procesos import EstadoProceso, Proceso


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


def _listos(procesos: list[Proceso]) -> list[Proceso]:
    return [proceso for proceso in procesos if proceso.estado == EstadoProceso.LISTO]


def _construir_tiempos(
    procesos: list[Proceso],
    inicio_por_pid: dict[int, int],
    fin_por_pid: dict[int, int],
) -> list[TiempoProceso]:
    tiempos: list[TiempoProceso] = []
    for proceso in sorted(procesos, key=lambda item: item.pid):
        if proceso.pid not in fin_por_pid:
            continue
        inicio = inicio_por_pid[proceso.pid]
        fin = fin_por_pid[proceso.pid]
        retorno = fin - proceso.llegada
        espera = retorno - proceso.cpu
        tiempos.append(
            TiempoProceso(
                pid=proceso.pid,
                nombre=proceso.nombre,
                llegada=proceso.llegada,
                cpu=proceso.cpu,
                inicio=inicio,
                fin=fin,
                retorno=retorno,
                espera=espera,
            )
        )
    return tiempos


def _promedios(tiempos: list[TiempoProceso]) -> tuple[float, float]:
    if not tiempos:
        return 0.0, 0.0
    cantidad = len(tiempos)
    return (
        sum(tiempo.retorno for tiempo in tiempos) / cantidad,
        sum(tiempo.espera for tiempo in tiempos) / cantidad,
    )


def _encolar_llegadas(
    pendientes: deque[Proceso],
    cola: deque[Proceso],
    t: int,
) -> None:
    while pendientes and pendientes[0].llegada <= t:
        cola.append(pendientes.popleft())


def _construir_resultado(
    algoritmo: str,
    quantum: int | None,
    ejecuciones: list[Ejecucion],
    tiempos: list[TiempoProceso],
) -> ResultadoPlanificacion:
    promedio_retorno, promedio_espera = _promedios(tiempos)
    return ResultadoPlanificacion(
        algoritmo=algoritmo,
        quantum=quantum,
        ejecuciones=ejecuciones,
        tiempos=tiempos,
        promedio_retorno=promedio_retorno,
        promedio_espera=promedio_espera,
    )


def fcfs(procesos: list[Proceso]) -> ResultadoPlanificacion:
    """Planifica primero en llegar, primero en ser atendido, sin expropiacion."""
    listos = sorted(_listos(procesos), key=lambda proceso: (proceso.llegada, proceso.pid))
    t = 0
    ejecuciones: list[Ejecucion] = []
    inicio_por_pid: dict[int, int] = {}
    fin_por_pid: dict[int, int] = {}

    for proceso in listos:
        inicio = max(t, proceso.llegada)
        fin = inicio + proceso.cpu
        ejecuciones.append(Ejecucion(proceso.pid, proceso.nombre, inicio, fin))
        inicio_por_pid[proceso.pid] = inicio
        fin_por_pid[proceso.pid] = fin
        t = fin

    tiempos = _construir_tiempos(listos, inicio_por_pid, fin_por_pid)
    return _construir_resultado("FCFS", None, ejecuciones, tiempos)


def sjf(procesos: list[Proceso]) -> ResultadoPlanificacion:
    """Planifica el trabajo mas corto primero, sin expropiacion."""
    listos = _listos(procesos)
    pendientes = list(listos)
    t = 0
    ejecuciones: list[Ejecucion] = []
    inicio_por_pid: dict[int, int] = {}
    fin_por_pid: dict[int, int] = {}

    while pendientes:
        disponibles = [
            proceso for proceso in pendientes if proceso.llegada <= t
        ]
        if not disponibles:
            t = min(proceso.llegada for proceso in pendientes)
            continue

        proceso = min(
            disponibles,
            key=lambda item: (item.cpu, item.llegada, item.pid),
        )
        inicio = t
        fin = t + proceso.cpu
        ejecuciones.append(Ejecucion(proceso.pid, proceso.nombre, inicio, fin))
        inicio_por_pid[proceso.pid] = inicio
        fin_por_pid[proceso.pid] = fin
        pendientes.remove(proceso)
        t = fin

    tiempos = _construir_tiempos(listos, inicio_por_pid, fin_por_pid)
    return _construir_resultado("SJF", None, ejecuciones, tiempos)


def rr(
    procesos: list[Proceso],
    quantum: int = 3,
) -> ResultadoPlanificacion:
    """Planifica Round Robin con turnos de quantum."""
    if not isinstance(quantum, int) or isinstance(quantum, bool) or quantum < 1:
        raise ValueError("El quantum debe ser un entero mayor o igual que 1")

    listos = _listos(procesos)
    pendientes: deque[Proceso] = deque(
        sorted(listos, key=lambda proceso: (proceso.llegada, proceso.pid))
    )
    cola: deque[Proceso] = deque()
    restante = {proceso.pid: proceso.cpu for proceso in listos}

    t = 0
    ejecuciones: list[Ejecucion] = []
    inicio_por_pid: dict[int, int] = {}
    fin_por_pid: dict[int, int] = {}

    while pendientes or cola:
        _encolar_llegadas(pendientes, cola, t)
        if not cola:
            t = pendientes[0].llegada
            continue

        proceso = cola.popleft()
        usar = min(quantum, restante[proceso.pid])
        inicio = t
        fin = t + usar
        ejecuciones.append(Ejecucion(proceso.pid, proceso.nombre, inicio, fin))
        if proceso.pid not in inicio_por_pid:
            inicio_por_pid[proceso.pid] = inicio

        restante[proceso.pid] -= usar
        t = fin
        _encolar_llegadas(pendientes, cola, t)

        if restante[proceso.pid] > 0:
            cola.append(proceso)
        else:
            fin_por_pid[proceso.pid] = fin

    tiempos = _construir_tiempos(listos, inicio_por_pid, fin_por_pid)
    return _construir_resultado("RR", quantum, ejecuciones, tiempos)


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
