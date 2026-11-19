import unittest

import memoria
import procesos
from procesos import EstadoProceso, Proceso


class TestProcesos(unittest.TestCase):
    def setUp(self):
        procesos.reiniciar_procesos()
        self.addCleanup(procesos.reiniciar_procesos)

    def test_crear_con_valores_por_defecto(self):
        proceso = procesos.crear_proceso("editor")

        self.assertEqual(proceso.pid, 1)
        self.assertEqual(proceso.nombre, "editor")
        self.assertEqual(proceso.llegada, 0)
        self.assertEqual(proceso.cpu, 1)
        self.assertEqual(proceso.prioridad, 1)
        self.assertEqual(proceso.memoria, 64)
        self.assertIs(proceso.estado, EstadoProceso.LISTO)
        self.assertEqual(memoria.estado_memoria().usada, 64)

    def test_pid_autoincremental_y_listado_ordenado(self):
        primero = procesos.crear_proceso("primero")
        segundo = procesos.crear_proceso("segundo", llegada=2, cpu=3)

        self.assertEqual((primero.pid, segundo.pid), (1, 2))
        self.assertEqual(
            [proceso.nombre for proceso in procesos.listar_procesos()],
            ["primero", "segundo"],
        )
        self.assertIs(procesos.consultar_proceso(1), primero)
        self.assertIs(procesos.consultar_proceso(2), segundo)
        self.assertIsNone(procesos.consultar_proceso(99))

    def test_nombre_duplicado_y_palabra_reservada(self):
        procesos.crear_proceso("editor")

        with self.assertRaises(ValueError):
            procesos.crear_proceso("editor")
        for nombre in ("cpu", "CPU", "planificar", "memoria"):
            with self.subTest(nombre=nombre):
                with self.assertRaises(ValueError):
                    procesos.crear_proceso(nombre)

        self.assertEqual(len(procesos.listar_procesos()), 1)
        self.assertEqual(memoria.estado_memoria().usada, 64)

    def test_nombres_invalidos(self):
        for nombre in ("", "1editor", "editor-1", "editor uno", "editor.txt", "á"):
            with self.subTest(nombre=nombre):
                with self.assertRaises(ValueError):
                    procesos.crear_proceso(nombre)
        self.assertEqual(procesos.listar_procesos(), [])

    def test_campos_invalidos(self):
        casos = (
            {"llegada": -1},
            {"cpu": 0},
            {"prioridad": -1},
            {"memoria": 0},
            {"llegada": True},
            {"cpu": False},
            {"memoria": 1.5},
        )
        for caso in casos:
            with self.subTest(caso=caso):
                with self.assertRaises(ValueError):
                    procesos.crear_proceso("valido", **caso)
        self.assertEqual(procesos.listar_procesos(), [])

    def test_proceso_valida_sus_campos(self):
        proceso = Proceso(1, "valido", 0, 1, 1, 64)
        self.assertIs(proceso.estado, EstadoProceso.NUEVO)

        with self.assertRaises(ValueError):
            Proceso(0, "valido", 0, 1, 1, 64)
        with self.assertRaises(ValueError):
            Proceso(1, "cpu", 0, 1, 1, 64)
        with self.assertRaises(ValueError):
            Proceso(1, "valido", -1, 1, 1, 64)

    def test_memoria_insuficiente_deja_proceso_rechazado(self):
        proceso = procesos.crear_proceso("grande", memoria=2000)

        self.assertIs(proceso.estado, EstadoProceso.RECHAZADO)
        self.assertEqual(memoria.estado_memoria().usada, 0)
        self.assertEqual(
            [item.pid for item in procesos.listar_procesos()],
            [proceso.pid],
        )
        with self.assertRaises(ValueError):
            procesos.finalizar_proceso(proceso.pid)

    def test_finalizar_libera_memoria_y_es_terminal(self):
        proceso = procesos.crear_proceso("editor", memoria=128)
        self.assertEqual(memoria.estado_memoria().usada, 128)

        finalizado = procesos.finalizar_proceso(proceso.pid)

        self.assertIs(finalizado, proceso)
        self.assertIs(proceso.estado, EstadoProceso.TERMINADO)
        self.assertEqual(memoria.estado_memoria().usada, 0)
        self.assertIsNone(procesos.finalizar_proceso(99))
        with self.assertRaises(ValueError):
            procesos.finalizar_proceso(proceso.pid)

    def test_pid_no_se_reutiliza(self):
        primero = procesos.crear_proceso("primero")
        procesos.finalizar_proceso(primero.pid)
        segundo = procesos.crear_proceso("segundo")

        self.assertEqual(primero.pid, 1)
        self.assertEqual(segundo.pid, 2)
        self.assertEqual(segundo.estado, EstadoProceso.LISTO)

    def test_finalizar_proceso_en_ejecucion(self):
        proceso = procesos.crear_proceso("editor", memoria=64)
        proceso.estado = EstadoProceso.EJECUTANDO

        procesos.finalizar_proceso(proceso.pid)

        self.assertIs(proceso.estado, EstadoProceso.TERMINADO)
        self.assertEqual(memoria.estado_memoria().usada, 0)

    def test_cargar_ejemplo_reinicia_y_carga_p1_p4(self):
        procesos.crear_proceso("anterior", memoria=900)

        ejemplo = procesos.cargar_ejemplo()

        self.assertEqual([proceso.pid for proceso in ejemplo], [1, 2, 3, 4])
        self.assertEqual(
            [proceso.nombre for proceso in ejemplo],
            ["P1", "P2", "P3", "P4"],
        )
        self.assertEqual(
            [(proceso.llegada, proceso.cpu, proceso.prioridad, proceso.memoria)
             for proceso in ejemplo],
            [(0, 8, 2, 128), (1, 4, 1, 64), (2, 9, 3, 256), (3, 5, 2, 100)],
        )
        self.assertTrue(all(proceso.estado is EstadoProceso.LISTO for proceso in ejemplo))
        self.assertEqual(memoria.estado_memoria().usada, 548)
        self.assertEqual(len(procesos.listar_procesos()), 4)

    def test_cargar_ejemplo_no_reutiliza_pids(self):
        procesos.crear_proceso("anterior", memoria=10)
        procesos.cargar_ejemplo()
        nuevo = procesos.crear_proceso("nuevo")

        self.assertEqual(nuevo.pid, 5)
        self.assertEqual(memoria.estado_memoria().usada, 548 + 64)


if __name__ == "__main__":
    unittest.main()
