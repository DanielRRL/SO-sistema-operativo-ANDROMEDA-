"""Demostracion de concurrencia y sincronizacion. Stub temporal de T1.3."""

from dataclasses import dataclass


MODOS = ("sin_lock", "con_lock", "semaforo")


@dataclass(frozen=True)
class ResultadoConcurrencia:
    """Resultado de una demostracion de concurrencia."""

    modo: str
    valor_esperado: int
    valor_obtenido: int
    correcto: bool
    detalle: str


def ejecutar_concurrencia(
    modo: str,
    hilos: int = 4,
    iteraciones: int = 1000,
) -> ResultadoConcurrencia:
    """Devuelve un resultado falso segun el modo solicitado.

    Stub T1.3: la implementacion con hilos reales corresponde a T3.11.
    """
    modo_normalizado = modo.lower()
    if modo_normalizado not in MODOS:
        raise ValueError(f"Modo de concurrencia no reconocido: {modo}")
    esperado = hilos * iteraciones
    if modo_normalizado == "sin_lock":
        return ResultadoConcurrencia(
            modo=modo_normalizado,
            valor_esperado=esperado,
            valor_obtenido=esperado - 1,
            correcto=False,
            detalle="Stub: condicion de carrera simulada.",
        )
    return ResultadoConcurrencia(
        modo=modo_normalizado,
        valor_esperado=esperado,
        valor_obtenido=esperado,
        correcto=True,
        detalle="Stub: acceso protegido simulado.",
    )
