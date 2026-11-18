import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import archivos
from consola import ayuda, despachar, mostrar_tokens
from main import ejecutar_linea
from memoria import (
    CAPACIDAD_TOTAL,
    estado_memoria,
    liberar,
    reiniciar_memoria,
    reservar,
)
from parser import Orden


class TestAyudaYTokens(unittest.TestCase):
    def test_ayuda_general_y_especifica(self):
        general = ayuda()
        especifica = ayuda("PLANIFICAR")

        self.assertIn("Comandos disponibles", general)
        self.assertIn("planificar", general)
        self.assertIn("Round Robin", especifica)
        self.assertIn("Ejemplo:", especifica)

    def test_ayuda_palabra_desconocida(self):
        self.assertTrue(ayuda("no_existe").startswith("[ERROR]"))

    def test_tokens_lista_terminales_si_no_hay_texto(self):
        salida = mostrar_tokens()

        self.assertIn("Terminales reconocidos", salida)
        self.assertIn("CREAR", salida)
        self.assertIn("NOMBRE_ARCHIVO", salida)

    def test_tokens_analiza_entrada_y_reporta_error(self):
        salida = mostrar_tokens("crear proceso @x")

        self.assertTrue(salida.startswith("[ERROR]"))
        self.assertIn("CREAR", salida)
        self.assertIn("ERROR", salida)
        self.assertIn("columna 15", salida)

    def test_despacho_de_ayuda_y_tokens(self):
        ayuda_orden = Orden(comando="ayuda", argumentos=("planificar",))
        tokens_orden = Orden(comando="tokens", argumentos=("salir",))

        self.assertIn("Round Robin", despachar(ayuda_orden))
        self.assertIn("SALIR", despachar(tokens_orden))

    def test_comandos_disponibles_desde_main(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            self.assertTrue(ejecutar_linea("ayuda planificar"))
            self.assertTrue(ejecutar_linea("tokens salir"))

        self.assertIn("Round Robin", salida.getvalue())
        self.assertIn("SALIR", salida.getvalue())


class TestMemoria(unittest.TestCase):
    def setUp(self):
        reiniciar_memoria()
        self.addCleanup(reiniciar_memoria)

    def test_reserva_estado_y_liberacion(self):
        self.assertTrue(reservar(1, 256))
        estado = estado_memoria()

        self.assertEqual(estado.total, CAPACIDAD_TOTAL)
        self.assertEqual(estado.usada, 256)
        self.assertEqual(estado.libre, 768)
        self.assertEqual(estado.asignaciones, {1: 256})
        self.assertEqual(liberar(1), 256)
        self.assertEqual(estado_memoria().libre, CAPACIDAD_TOTAL)

    def test_rechaza_exceso_y_no_modifica_estado(self):
        self.assertFalse(reservar(1, CAPACIDAD_TOTAL + 1))
        self.assertEqual(estado_memoria().usada, 0)

        self.assertTrue(reservar(1, CAPACIDAD_TOTAL))
        self.assertFalse(reservar(2, 1))
        self.assertEqual(estado_memoria().usada, CAPACIDAD_TOTAL)

    def test_rechaza_datos_invalidos_y_asignacion_duplicada(self):
        with self.assertRaises(ValueError):
            reservar(0, 10)
        with self.assertRaises(ValueError):
            reservar(1, 0)

        self.assertTrue(reservar(1, 10))
        self.assertFalse(reservar(1, 20))
        self.assertEqual(estado_memoria().asignaciones, {1: 10})

    def test_liberar_pid_inexistente(self):
        self.assertEqual(liberar(999), 0)


class TestArchivos(unittest.TestCase):
    def setUp(self):
        self.directorio_temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.directorio_temporal.cleanup)
        self.parche_carpeta = patch(
            "archivos.CARPETA_PRUEBAS",
            Path(self.directorio_temporal.name) / "carpeta_pruebas",
        )
        self.parche_carpeta.start()
        self.addCleanup(self.parche_carpeta.stop)

    def test_operaciones_basicas(self):
        creado = archivos.crear_archivo("notas.txt", "hola")
        self.assertEqual(creado.nombre, "notas.txt")
        self.assertEqual(archivos.leer_archivo("notas.txt"), "hola")

        modificado = archivos.modificar_archivo("notas.txt", " mundo")
        self.assertEqual(modificado.tamano, len("hola mundo"))
        self.assertEqual(archivos.leer_archivo("notas.txt"), "hola mundo")
        self.assertTrue(archivos.existe_archivo("notas.txt"))
        self.assertEqual([info.nombre for info in archivos.listar_archivos()], ["notas.txt"])
        self.assertTrue(archivos.eliminar_archivo("notas.txt"))
        self.assertFalse(archivos.existe_archivo("notas.txt"))
        self.assertFalse(archivos.eliminar_archivo("notas.txt"))

    def test_rechaza_rutas_y_nombres_reservados(self):
        for nombre in ("../secreto.txt", "sub/archivo.txt", r"..\secreto.txt", "C:\\secreto.txt", "crear.txt"):
            with self.subTest(nombre=nombre):
                with self.assertRaises(ValueError):
                    archivos.validar_nombre(nombre)

    def test_operaciones_sobre_archivos_inexistentes(self):
        with self.assertRaises(FileNotFoundError):
            archivos.leer_archivo("falta.txt")
        with self.assertRaises(FileNotFoundError):
            archivos.modificar_archivo("falta.txt", "texto")

    def test_crear_no_sobrescribe(self):
        archivos.crear_archivo("nota.txt", "original")

        with self.assertRaises(FileExistsError):
            archivos.crear_archivo("nota.txt", "nuevo")

        self.assertEqual(archivos.leer_archivo("nota.txt"), "original")


if __name__ == "__main__":
    unittest.main()
