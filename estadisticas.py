"""Calculo y formato de estadisticas. Stub temporal de T1.3."""

from dataclasses import dataclass

from planificador import ResultadoPlanificacion, TiempoProceso


@dataclass(frozen=True)
class Estadisticas:
    """Tiempos y promedios de una planificacion."""

    algoritmo: str
    tiempos: list[TiempoProceso]
    promedio_retorno: float
    promedio_espera: float


def calcular_estadisticas(resultado: ResultadoPlanificacion) -> Estadisticas:
    """Devuelve estadisticas vacias.

    Stub T1.3: la implementacion real corresponde a T3.4.
    """
    return Estadisticas(
        algoritmo=resultado.algoritmo,
        tiempos=[],
        promedio_retorno=0.0,
        promedio_espera=0.0,
    )


def formatear_estadisticas(estadisticas: Estadisticas) -> str:
    """Devuelve un mensaje temporal de estadisticas."""
    return f"[OK] Estadisticas pendientes para {estadisticas.algoritmo}."
