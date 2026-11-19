import unittest

from planificador import fcfs, planificar, rr, sjf
from procesos import EstadoProceso, Proceso


def ejemplo():
    return [
        Proceso(1, "P1", 0, 8, 2, 128, EstadoProceso.LISTO),
        Proceso(2, "P2", 1, 4, 1, 64, EstadoProceso.LISTO),
        Proceso(3, "P3", 2, 9, 3, 256, EstadoProceso.LISTO),
        Proceso(4, "P4", 3, 5, 2, 100, EstadoProceso.LISTO),
    ]


def gantt(resultado):
    return [(ejecucion.pid, ejecucion.inicio, ejecucion.fin) for ejecucion in resultado.ejecuciones]


def tiempos(resultado):
    return [
        (tiempo.pid, tiempo.inicio, tiempo.fin, tiempo.retorno, tiempo.espera)
        for tiempo in resultado.tiempos
    ]


class TestFCFS(unittest.TestCase):
    def test_ejemplo_p1_p4(self):
        resultado = fcfs(ejemplo())

        self.assertEqual(resultado.algoritmo, "FCFS")
        self.assertIsNone(resultado.quantum)
        self.assertEqual(
            gantt(resultado),
            [(1, 0, 8), (2, 8, 12), (3, 12, 21), (4, 21, 26)],
        )
        self.assertEqual(
            tiempos(resultado),
            [
                (1, 0, 8, 8, 0),
                (2, 8, 12, 11, 7),
                (3, 12, 21, 19, 10),
                (4, 21, 26, 23, 18),
            ],
        )
        self.assertEqual(resultado.promedio_retorno, 15.25)
        self.assertEqual(resultado.promedio_espera, 8.75)

    def test_orden_por_llegada_y_pid(self):
        procesos = [
            Proceso(2, "P2", 0, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(1, "P1", 0, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(3, "P3", 1, 1, 1, 10, EstadoProceso.LISTO),
        ]
        self.assertEqual(
            gantt(fcfs(procesos)),
            [(1, 0, 2), (2, 2, 4), (3, 4, 5)],
        )

    def test_avanza_hasta_la_primera_llegada(self):
        procesos = [
            Proceso(1, "P1", 5, 2, 1, 10, EstadoProceso.LISTO),
        ]
        resultado = fcfs(procesos)

        self.assertEqual(gantt(resultado), [(1, 5, 7)])
        self.assertEqual(tiempos(resultado), [(1, 5, 7, 2, 0)])

    def test_sin_procesos_listos(self):
        procesos = [
            Proceso(1, "P1", 0, 5, 1, 10, EstadoProceso.RECHAZADO),
            Proceso(2, "P2", 0, 5, 1, 10, EstadoProceso.TERMINADO),
        ]
        resultado = fcfs(procesos)

        self.assertEqual(resultado.ejecuciones, [])
        self.assertEqual(resultado.tiempos, [])
        self.assertEqual(resultado.promedio_retorno, 0.0)
        self.assertEqual(resultado.promedio_espera, 0.0)

    def test_no_modifica_los_procesos(self):
        procesos = ejemplo()
        antes = [(p.pid, p.estado, p.cpu, p.llegada) for p in procesos]
        fcfs(procesos)
        despues = [(p.pid, p.estado, p.cpu, p.llegada) for p in procesos]

        self.assertEqual(antes, despues)


class TestSJF(unittest.TestCase):
    def test_ejemplo_p1_p4(self):
        resultado = sjf(ejemplo())

        self.assertEqual(resultado.algoritmo, "SJF")
        self.assertIsNone(resultado.quantum)
        self.assertEqual(
            gantt(resultado),
            [(1, 0, 8), (2, 8, 12), (4, 12, 17), (3, 17, 26)],
        )
        self.assertEqual(
            tiempos(resultado),
            [
                (1, 0, 8, 8, 0),
                (2, 8, 12, 11, 7),
                (3, 17, 26, 24, 15),
                (4, 12, 17, 14, 9),
            ],
        )
        self.assertEqual(resultado.promedio_retorno, 14.25)
        self.assertEqual(resultado.promedio_espera, 7.75)

    def test_no_es_expulsivo(self):
        procesos = [
            Proceso(1, "P1", 0, 10, 1, 10, EstadoProceso.LISTO),
            Proceso(2, "P2", 1, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(3, "P3", 2, 3, 1, 10, EstadoProceso.LISTO),
        ]
        self.assertEqual(
            gantt(sjf(procesos)),
            [(1, 0, 10), (2, 10, 12), (3, 12, 15)],
        )

    def test_empate_por_pid(self):
        procesos = [
            Proceso(2, "P2", 0, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(1, "P1", 0, 2, 1, 10, EstadoProceso.LISTO),
        ]
        self.assertEqual(
            gantt(sjf(procesos)),
            [(1, 0, 2), (2, 2, 4)],
        )

    def test_avanza_hasta_la_primera_llegada(self):
        procesos = [
            Proceso(1, "P1", 5, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(2, "P2", 5, 1, 1, 10, EstadoProceso.LISTO),
        ]
        self.assertEqual(
            gantt(sjf(procesos)),
            [(2, 5, 6), (1, 6, 8)],
        )

    def test_ignora_procesos_no_listos(self):
        procesos = [
            Proceso(1, "P1", 0, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(2, "P2", 0, 1, 1, 10, EstadoProceso.RECHAZADO),
        ]
        self.assertEqual(gantt(sjf(procesos)), [(1, 0, 2)])
        self.assertEqual([tiempo.pid for tiempo in sjf(procesos).tiempos], [1])


class TestRoundRobin(unittest.TestCase):
    def test_ejemplo_quantum_3(self):
        resultado = rr(ejemplo(), quantum=3)

        self.assertEqual(resultado.algoritmo, "RR")
        self.assertEqual(resultado.quantum, 3)
        self.assertEqual(
            gantt(resultado),
            [
                (1, 0, 3),
                (2, 3, 6),
                (3, 6, 9),
                (4, 9, 12),
                (1, 12, 15),
                (2, 15, 16),
                (3, 16, 19),
                (4, 19, 21),
                (1, 21, 23),
                (3, 23, 26),
            ],
        )
        self.assertEqual(
            tiempos(resultado),
            [
                (1, 0, 23, 23, 15),
                (2, 3, 16, 15, 11),
                (3, 6, 26, 24, 15),
                (4, 9, 21, 18, 13),
            ],
        )
        self.assertEqual(resultado.promedio_retorno, 20.0)
        self.assertEqual(resultado.promedio_espera, 13.5)

    def test_quantum_configurable_2(self):
        resultado = rr(ejemplo(), quantum=2)

        self.assertEqual(
            gantt(resultado),
            [
                (1, 0, 2),
                (2, 2, 4),
                (3, 4, 6),
                (1, 6, 8),
                (4, 8, 10),
                (2, 10, 12),
                (3, 12, 14),
                (1, 14, 16),
                (4, 16, 18),
                (3, 18, 20),
                (1, 20, 22),
                (4, 22, 23),
                (3, 23, 25),
                (3, 25, 26),
            ],
        )
        self.assertEqual(
            tiempos(resultado),
            [
                (1, 0, 22, 22, 14),
                (2, 2, 12, 11, 7),
                (3, 4, 26, 24, 15),
                (4, 8, 23, 20, 15),
            ],
        )
        self.assertEqual(resultado.promedio_retorno, 19.25)
        self.assertEqual(resultado.promedio_espera, 12.75)

    def test_llegada_justo_al_final_del_quantum(self):
        procesos = [
            Proceso(1, "P1", 0, 4, 1, 10, EstadoProceso.LISTO),
            Proceso(2, "P2", 3, 1, 1, 10, EstadoProceso.LISTO),
        ]
        self.assertEqual(
            gantt(rr(procesos, quantum=3)),
            [(1, 0, 3), (2, 3, 4), (1, 4, 5)],
        )

    def test_avanza_hasta_la_primera_llegada(self):
        procesos = [
            Proceso(1, "P1", 5, 4, 1, 10, EstadoProceso.LISTO),
            Proceso(2, "P2", 5, 2, 1, 10, EstadoProceso.LISTO),
        ]
        self.assertEqual(
            gantt(rr(procesos, quantum=3)),
            [(1, 5, 8), (2, 8, 10), (1, 10, 11)],
        )

    def test_ignora_procesos_no_listos(self):
        procesos = [
            Proceso(1, "P1", 0, 2, 1, 10, EstadoProceso.LISTO),
            Proceso(2, "P2", 0, 1, 1, 10, EstadoProceso.RECHAZADO),
        ]
        resultado = rr(procesos)
        self.assertEqual(gantt(resultado), [(1, 0, 2)])
        self.assertEqual([tiempo.pid for tiempo in resultado.tiempos], [1])

    def test_sin_procesos_listos(self):
        resultado = rr([])
        self.assertEqual(resultado.algoritmo, "RR")
        self.assertEqual(resultado.quantum, 3)
        self.assertEqual(resultado.ejecuciones, [])
        self.assertEqual(resultado.tiempos, [])
        self.assertEqual(resultado.promedio_retorno, 0.0)
        self.assertEqual(resultado.promedio_espera, 0.0)

    def test_no_modifica_los_procesos(self):
        procesos = ejemplo()
        antes = [(p.pid, p.estado, p.cpu, p.llegada) for p in procesos]
        rr(procesos)
        despues = [(p.pid, p.estado, p.cpu, p.llegada) for p in procesos]
        self.assertEqual(antes, despues)

    def test_quantum_invalido(self):
        for quantum in (0, -1, True, 1.5):
            with self.subTest(quantum=quantum):
                with self.assertRaises(ValueError):
                    rr(ejemplo(), quantum=quantum)

    def test_planificar_rr(self):
        resultado = planificar(ejemplo(), "rr", quantum=2)
        self.assertEqual(resultado.algoritmo, "RR")
        self.assertEqual(resultado.quantum, 2)


class TestDespacho(unittest.TestCase):
    def test_planificar_llama_a_fcfs_y_sjf(self):
        self.assertEqual(planificar(ejemplo(), "fcfs").algoritmo, "FCFS")
        self.assertEqual(planificar(ejemplo(), "sjf").algoritmo, "SJF")
        self.assertEqual(planificar(ejemplo(), "FCFS").algoritmo, "FCFS")

    def test_algoritmo_desconocido(self):
        with self.assertRaises(ValueError):
            planificar(ejemplo(), "lifo")


if __name__ == "__main__":
    unittest.main()
