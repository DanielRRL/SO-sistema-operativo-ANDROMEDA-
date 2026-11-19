import unittest

import memoria
import procesos


class TestIntegracionMemoriaProcesos(unittest.TestCase):
    def setUp(self):
        procesos.reiniciar_procesos()
        self.addCleanup(procesos.reiniciar_procesos)

    def test_crear_reserva_y_finalizar_libera(self):
        proceso = procesos.crear_proceso("editor", memoria=200)

        self.assertEqual(proceso.estado.value, "LISTO")
        self.assertEqual(memoria.estado_memoria().usada, 200)
        self.assertEqual(memoria.estado_memoria().asignaciones, {1: 200})

        procesos.finalizar_proceso(proceso.pid)

        self.assertEqual(proceso.estado.value, "TERMINADO")
        self.assertEqual(memoria.estado_memoria().usada, 0)
        self.assertEqual(memoria.estado_memoria().asignaciones, {})

    def test_capacidad_y_rechazo(self):
        primero = procesos.crear_proceso("primero", memoria=600)
        segundo = procesos.crear_proceso("segundo", memoria=424)
        rechazado = procesos.crear_proceso("tercero", memoria=1)

        self.assertEqual(primero.estado.value, "LISTO")
        self.assertEqual(segundo.estado.value, "LISTO")
        self.assertEqual(rechazado.estado.value, "RECHAZADO")
        self.assertEqual(memoria.estado_memoria().usada, 1024)
        self.assertEqual(memoria.estado_memoria().libre, 0)
        self.assertEqual(
            memoria.estado_memoria().asignaciones,
            {primero.pid: 600, segundo.pid: 424},
        )

    def test_rechazado_no_consume_memoria_ni_se_puede_finalizar(self):
        proceso = procesos.crear_proceso("grande", memoria=2000)

        self.assertEqual(proceso.estado.value, "RECHAZADO")
        self.assertEqual(memoria.estado_memoria().usada, 0)
        self.assertEqual(memoria.estado_memoria().asignaciones, {})
        self.assertIn(proceso, procesos.listar_procesos())

        with self.assertRaises(ValueError):
            procesos.finalizar_proceso(proceso.pid)
        self.assertEqual(memoria.estado_memoria().usada, 0)

    def test_liberacion_parcial(self):
        primero = procesos.crear_proceso("primero", memoria=128)
        segundo = procesos.crear_proceso("segundo", memoria=256)
        tercero = procesos.crear_proceso("tercero", memoria=100)

        self.assertEqual(memoria.estado_memoria().usada, 484)

        procesos.finalizar_proceso(segundo.pid)

        self.assertEqual(memoria.estado_memoria().usada, 228)
        self.assertEqual(
            memoria.estado_memoria().asignaciones,
            {primero.pid: 128, tercero.pid: 100},
        )
        self.assertEqual(segundo.estado.value, "TERMINADO")

    def test_reutiliza_memoria_liberada(self):
        primero = procesos.crear_proceso("primero", memoria=800)
        rechazado = procesos.crear_proceso("segundo", memoria=424)

        self.assertEqual(rechazado.estado.value, "RECHAZADO")
        procesos.finalizar_proceso(primero.pid)

        tercero = procesos.crear_proceso("tercero", memoria=1024)

        self.assertEqual(tercero.estado.value, "LISTO")
        self.assertEqual(memoria.estado_memoria().usada, 1024)
        self.assertEqual(memoria.estado_memoria().asignaciones, {tercero.pid: 1024})

    def test_cargar_ejemplo_resetea_memoria(self):
        procesos.crear_proceso("anterior", memoria=900)

        ejemplo = procesos.cargar_ejemplo()

        self.assertEqual([proceso.nombre for proceso in ejemplo], ["P1", "P2", "P3", "P4"])
        self.assertEqual(memoria.estado_memoria().usada, 548)
        self.assertEqual(
            memoria.estado_memoria().asignaciones,
            {1: 128, 2: 64, 3: 256, 4: 100},
        )
        self.assertEqual(len(procesos.listar_procesos()), 4)

    def test_creacion_invalida_no_reserva_memoria(self):
        with self.assertRaises(ValueError):
            procesos.crear_proceso("cpu")
        with self.assertRaises(ValueError):
            procesos.crear_proceso("valido", cpu=0)
        with self.assertRaises(ValueError):
            procesos.crear_proceso("valido", memoria=0)

        self.assertEqual(memoria.estado_memoria().usada, 0)
        self.assertEqual(memoria.estado_memoria().asignaciones, {})

        valido = procesos.crear_proceso("valido", memoria=64)
        self.assertEqual(valido.estado.value, "LISTO")
        self.assertEqual(memoria.estado_memoria().usada, 64)

    def test_reiniciar_procesos_libera_memoria_y_pid(self):
        procesos.crear_proceso("anterior", memoria=300)
        procesos.reiniciar_procesos()

        self.assertEqual(procesos.listar_procesos(), [])
        self.assertEqual(memoria.estado_memoria().usada, 0)
        self.assertEqual(memoria.estado_memoria().asignaciones, {})

        nuevo = procesos.crear_proceso("nuevo", memoria=10)
        self.assertEqual(nuevo.pid, 1)
        self.assertEqual(memoria.estado_memoria().usada, 10)


if __name__ == "__main__":
    unittest.main()
