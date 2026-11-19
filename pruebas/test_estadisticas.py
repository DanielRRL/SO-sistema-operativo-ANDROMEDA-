import unittest

from estadisticas import calcular_estadisticas, formatear_estadisticas
from planificador import (
    ResultadoPlanificacion,
    TiempoProceso,
    fcfs,
    rr,
    sjf,
)
from procesos import EstadoProceso, Proceso


def ejemplo():
    return [
        Proceso(1, "P1", 0, 8, 2, 128, EstadoProceso.LISTO),
        Proceso(2, "P2", 1, 4, 1, 64, EstadoProceso.LISTO),
        Proceso(3, "P3", 2, 9, 3, 256, EstadoProceso.LISTO),
        Proceso(4, "P4", 3, 5, 2, 100, EstadoProceso.LISTO),
    ]


def tiempos(resultado):
    return [
        (tiempo.pid, tiempo.fin, tiempo.retorno, tiempo.espera)
        for tiempo in resultado.tiempos
    ]


class TestEstadisticas(unittest.TestCase):
    def test_fcfs_calcula_tiempos_y_promedios(self):
        estadisticas = calcular_estadisticas(fcfs(ejemplo()))

        self.assertEqual(estadisticas.algoritmo, "FCFS")
        self.assertEqual(
            tiempos(estadisticas),
            [
                (1, 8, 8, 0),
                (2, 12, 11, 7),
                (3, 21, 19, 10),
                (4, 26, 23, 18),
            ],
        )
        self.assertEqual(estadisticas.promedio_retorno, 15.25)
        self.assertEqual(estadisticas.promedio_espera, 8.75)

    def test_sjf_calcula_promedios(self):
        estadisticas = calcular_estadisticas(sjf(ejemplo()))

        self.assertEqual(estadisticas.algoritmo, "SJF")
        self.assertEqual(estadisticas.promedio_retorno, 14.25)
        self.assertEqual(estadisticas.promedio_espera, 7.75)

    def test_rr_calcula_promedios(self):
        estadisticas = calcular_estadisticas(rr(ejemplo(), quantum=3))

        self.assertEqual(estadisticas.algoritmo, "RR")
        self.assertEqual(estadisticas.promedio_retorno, 20.0)
        self.assertEqual(estadisticas.promedio_espera, 13.5)

    def test_sin_tiempos(self):
        estadisticas = calcular_estadisticas(fcfs([]))

        self.assertEqual(estadisticas.algoritmo, "FCFS")
        self.assertEqual(estadisticas.tiempos, [])
        self.assertEqual(estadisticas.promedio_retorno, 0.0)
        self.assertEqual(estadisticas.promedio_espera, 0.0)
        self.assertEqual(
            formatear_estadisticas(estadisticas),
            "[OK] No hay procesos planificados.",
        )

    def test_formato_incluye_tabla_y_dos_decimales(self):
        salida = formatear_estadisticas(calcular_estadisticas(fcfs(ejemplo())))

        self.assertTrue(salida.startswith("[OK] Estadisticas de FCFS"))
        self.assertIn("PID", salida)
        self.assertIn("P1", salida)
        self.assertIn("P4", salida)
        self.assertIn("Promedio retorno: 15.25", salida)
        self.assertIn("Promedio espera:  8.75", salida)

    def test_formato_rr_dos_decimales(self):
        salida = formatear_estadisticas(
            calcular_estadisticas(rr(ejemplo(), quantum=3))
        )

        self.assertIn("Promedio retorno: 20.00", salida)
        self.assertIn("Promedio espera:  13.50", salida)

    def test_ordena_tiempos_por_pid_y_no_altera_el_resultado(self):
        resultado = ResultadoPlanificacion(
            algoritmo="FCFS",
            quantum=None,
            ejecuciones=[],
            tiempos=[
                TiempoProceso(2, "P2", 1, 4, 8, 12, 11, 7),
                TiempoProceso(1, "P1", 0, 8, 0, 8, 8, 0),
            ],
            promedio_retorno=0.0,
            promedio_espera=0.0,
        )
        originales = list(resultado.tiempos)

        estadisticas = calcular_estadisticas(resultado)

        self.assertEqual([tiempo.pid for tiempo in estadisticas.tiempos], [1, 2])
        self.assertEqual(resultado.tiempos, originales)
        self.assertEqual(estadisticas.promedio_retorno, 9.5)
        self.assertEqual(estadisticas.promedio_espera, 3.5)


if __name__ == "__main__":
    unittest.main()
