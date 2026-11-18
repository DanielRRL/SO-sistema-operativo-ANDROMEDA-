"""Demostracion de concurrencia y sincronizacion (T3.11).

Lanza varios hilos que incrementan un contador compartido en tres modos:

- sin_lock: sin proteccion; puede producir una condicion de carrera.
- con_lock: la seccion critica se protege con threading.Lock.
- semaforo: la seccion critica se protege con threading.Semaphore(1).

Se muestra el valor esperado (hilos * iteraciones) y el obtenido.
"""

import threading
import time
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


class _Contador:
    """Recurso compartido. El incremento se separa en lectura y escritura
    para que la condicion de carrera sea visible de forma fiable."""

    def __init__(self) -> None:
        self.valor = 0


def _incrementar_sin_proteccion(contador: _Contador, iteraciones: int) -> None:
    for _ in range(iteraciones):
        actual = contador.valor          # lee
        # Cede el procesador entre la lectura y la escritura: otro hilo
        # puede modificar el contador y este hilo sobrescribira su cambio.
        time.sleep(0)
        contador.valor = actual + 1      # escribe


def _incrementar_protegido(contador: _Contador, iteraciones: int, mecanismo) -> None:
    """Misma operacion, pero dentro de la seccion critica (with mecanismo)."""
    for _ in range(iteraciones):
        with mecanismo:                  # entrada y salida de la seccion critica
            actual = contador.valor
            time.sleep(0)
            contador.valor = actual + 1


def ejecutar_concurrencia(
    modo: str,
    hilos: int = 4,
    iteraciones: int = 1000,
) -> ResultadoConcurrencia:
    """Ejecuta la demostracion y devuelve valor esperado y obtenido.

    Lanza ValueError si el modo no existe o si hilos/iteraciones son < 1.
    """
    modo_normalizado = modo.lower()
    if modo_normalizado not in MODOS:
        raise ValueError(f"Modo de concurrencia no reconocido: {modo}")
    if hilos < 1 or iteraciones < 1:
        raise ValueError("hilos e iteraciones deben ser al menos 1.")

    contador = _Contador()
    if modo_normalizado == "sin_lock":
        objetivo, extra = _incrementar_sin_proteccion, ()
    elif modo_normalizado == "con_lock":
        objetivo, extra = _incrementar_protegido, (threading.Lock(),)
    else:
        objetivo, extra = _incrementar_protegido, (threading.Semaphore(1),)

    lista = [
        threading.Thread(target=objetivo, args=(contador, iteraciones) + extra)
        for _ in range(hilos)
    ]
    for hilo in lista:
        hilo.start()
    for hilo in lista:
        hilo.join()

    esperado = hilos * iteraciones
    obtenido = contador.valor
    correcto = obtenido == esperado

    if modo_normalizado == "sin_lock":
        if correcto:
            detalle = ("Sin proteccion, pero esta vez no hubo colision; "
                       "la condicion de carrera no esta garantizada.")
        else:
            detalle = (f"Condicion de carrera: se perdieron "
                       f"{esperado - obtenido} incrementos.")
    elif modo_normalizado == "con_lock":
        detalle = "El Lock permite un solo hilo en la seccion critica."
    else:
        detalle = "El Semaphore(1) permite un solo hilo en la seccion critica."

    return ResultadoConcurrencia(
        modo=modo_normalizado,
        valor_esperado=esperado,
        valor_obtenido=obtenido,
        correcto=correcto,
        detalle=detalle,
    )


def formatear_resultado(r: ResultadoConcurrencia) -> str:
    """Texto para la consola, con prefijo [OK] o [ERROR]."""
    estado = "[OK]" if r.correcto else "[ERROR]"
    return (
        f"{estado} Modo {r.modo}\n"
        f"  Valor esperado: {r.valor_esperado}\n"
        f"  Valor obtenido: {r.valor_obtenido}\n"
        f"  {r.detalle}"
    )
