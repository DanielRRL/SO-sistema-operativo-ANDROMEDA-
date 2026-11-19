import unittest

from estadisticas import calcular_estadisticas
from planificador import fcfs, rr, sjf
from procesos import EstadoProceso, Proceso


def proceso(pid, nombre, llegada, cpu):
    return Proceso(pid, nombre, llegada, cpu, 1, 10, EstadoProceso.LISTO)


def gantt(resultado):
    return [
        (ejecucion.pid, ejecucion.inicio, ejecucion.fin)
        for ejecucion in resultado.ejecuciones
    ]


def tiempos(resultado):
    return [
        (tiempo.pid, tiempo.inicio, tiempo.fin, tiempo.retorno, tiempo.espera)
        for tiempo in resultado.tiempos
    ]


class TestCasosBordePlanificacion(unittest.TestCase):
    def test_un_solo_proceso_fcfs(self):
        resultado = fcfs([proceso(1, "P1", 2, 3)])
        self.assertEqual(gantt(resultado), [(1, 2, 5)])
        self.assertEqual(tiempos(resultado), [(1, 2, 5, 3, 0)])
        estadisticas = calcular_estadisticas(resultado)
        self.assertEqual(estadisticas.promedio_retorno, 3.0)
        self.assertEqual(estadisticas.promedio_espera, 0.0)

    def test_un_solo_proceso_sjf(self):
        resultado = sjf([proceso(1, "P1", 2, 3)])
        self.assertEqual(gantt(resultado), [(1, 2, 5)])
        self.assertEqual(tiempos(resultado), [(1, 2, 5, 3, 0)])
        estadisticas = calcular_estadisticas(resultado)
        self.assertEqual(estadisticas.promedio_retorno, 3.0)
        self.assertEqual(estadisticas.promedio_espera, 0.0)

    def test_un_solo_proceso_rr(self):
        resultado = rr([proceso(1, "P1", 2, 3)], quantum=3)
        self.assertEqual(gantt(resultado), [(1, 2, 5)])
        self.assertEqual(tiempos(resultado), [(1, 2, 5, 3, 0)])
        estadisticas = calcular_estadisticas(resultado)
        self.assertEqual(estadisticas.promedio_retorno, 3.0)
        self.assertEqual(estadisticas.promedio_espera, 0.0)

    def test_cpu_ociosa_entre_procesos(self):
        procesos = [proceso(1, "P1", 0, 2), proceso(2, "P2", 5, 2)]
        esperado = [(1, 0, 2), (2, 5, 7)]
        for nombre, algoritmo in (
            ("FCFS", fcfs),
            ("SJF", sjf),
            ("RR", lambda items: rr(items, quantum=2)),
        ):
            with self.subTest(algoritmo=nombre):
                resultado = algoritmo(procesos)
                self.assertEqual(gantt(resultado), esperado)
                self.assertEqual(
                    tiempos(resultado),
                    [(1, 0, 2, 2, 0), (2, 5, 7, 2, 0)],
                )
                estadisticas = calcular_estadisticas(resultado)
                self.assertEqual(estadisticas.promedio_retorno, 2.0)
                self.assertEqual(estadisticas.promedio_espera, 0.0)
                self.assertFalse(
                    any(inicio <= 2 < fin for _, inicio, fin in gantt(resultado))
                )

    def test_rr_quantum_1(self):
        procesos = [proceso(1, "P1", 0, 3), proceso(2, "P2", 0, 2)]
        resultado = rr(procesos, quantum=1)

        self.assertEqual(
            gantt(resultado),
            [(1, 0, 1), (2, 1, 2), (1, 2, 3), (2, 3, 4), (1, 4, 5)],
        )
        self.assertEqual(
            tiempos(resultado),
            [(1, 0, 5, 5, 2), (2, 1, 4, 4, 2)],
        )
        estadisticas = calcular_estadisticas(resultado)
        self.assertEqual(estadisticas.promedio_retorno, 4.5)
        self.assertEqual(estadisticas.promedio_espera, 2.0)

    def test_rr_quantum_mayor_que_cpu(self):
        resultado = rr([proceso(1, "P1", 1, 2)], quantum=10)
        self.assertEqual(gantt(resultado), [(1, 1, 3)])
        self.assertEqual(tiempos(resultado), [(1, 1, 3, 2, 0)])

    def test_rr_llegada_al_borde_del_quantum(self):
        procesos = [proceso(1, "P1", 0, 4), proceso(2, "P2", 3, 1)]
        resultado = rr(procesos, quantum=3)

        self.assertEqual(
            gantt(resultado),
            [(1, 0, 3), (2, 3, 4), (1, 4, 5)],
        )
        self.assertEqual(
            tiempos(resultado),
            [(1, 0, 5, 5, 1), (2, 3, 4, 1, 0)],
        )
        estadisticas = calcular_estadisticas(resultado)
        self.assertEqual(estadisticas.promedio_retorno, 3.0)
        self.assertEqual(estadisticas.promedio_espera, 0.5)

    def test_lista_vacia_en_los_tres_algoritmos(self):
        for nombre, algoritmo in (
            ("FCFS", fcfs),
            ("SJF", sjf),
            ("RR", rr),
        ):
            with self.subTest(algoritmo=nombre):
                resultado = algoritmo([])
                self.assertEqual(resultado.ejecuciones, [])
                self.assertEqual(resultado.tiempos, [])
                self.assertEqual(resultado.promedio_retorno, 0.0)
                self.assertEqual(resultado.promedio_espera, 0.0)


if __name__ == "__main__":
    unittest.main()
