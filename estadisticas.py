"""Calculo y formato de estadisticas de planificacion."""

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
    """Calcula tiempos ordenados y promedios a partir de una planificacion."""
    tiempos = sorted(resultado.tiempos, key=lambda tiempo: tiempo.pid)
    if not tiempos:
        return Estadisticas(
            algoritmo=resultado.algoritmo,
            tiempos=[],
            promedio_retorno=0.0,
            promedio_espera=0.0,
        )

    cantidad = len(tiempos)
    return Estadisticas(
        algoritmo=resultado.algoritmo,
        tiempos=tiempos,
        promedio_retorno=sum(tiempo.retorno for tiempo in tiempos) / cantidad,
        promedio_espera=sum(tiempo.espera for tiempo in tiempos) / cantidad,
    )


def formatear_estadisticas(estadisticas: Estadisticas) -> str:
    """Devuelve una tabla con finalizacion, retorno, espera y promedios."""
    if not estadisticas.tiempos:
        return "[OK] No hay procesos planificados."

    lineas = [
        f"[OK] Estadisticas de {estadisticas.algoritmo}",
        f"{'PID':>4} {'Nombre':<12} {'Fin':>6} {'Retorno':>8} {'Espera':>7}",
    ]
    for tiempo in estadisticas.tiempos:
        lineas.append(
            f"{tiempo.pid:>4} {tiempo.nombre:<12} {tiempo.fin:>6} "
            f"{tiempo.retorno:>8} {tiempo.espera:>7}"
        )
    lineas.append("")
    lineas.append(f"Promedio retorno: {estadisticas.promedio_retorno:.2f}")
    lineas.append(f"Promedio espera:  {estadisticas.promedio_espera:.2f}")
    return "\n".join(lineas)
