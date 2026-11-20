"""Pruebas de casos de error de la consola (T5.3).

Verifican que ninguna entrada invalida muestre un error tecnico (traceback,
excepcion sin manejar) y que el bucle del simulador siga funcionando.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import archivos
import consola
import memoria
import mensajes
import procesos
from main import ejecutar_linea


class TestCasosDeErrorConsola(unittest.TestCase):
    def setUp(self):
        procesos.reiniciar_procesos()
        mensajes.limpiar()
        consola._ultimo_resultado = None
        self.addCleanup(procesos.reiniciar_procesos)
        self.addCleanup(mensajes.limpiar)
        self.addCleanup(setattr, consola, "_ultimo_resultado", None)

        self.directorio_temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.directorio_temporal.cleanup)
        self.raiz = Path(self.directorio_temporal.name)
        self.parche_carpeta = patch(
            "archivos.CARPETA_PRUEBAS", self.raiz / "carpeta_pruebas"
        )
        self.parche_carpeta.start()
        self.addCleanup(self.parche_carpeta.stop)

    def ejecutar(self, linea):
        """Ejecuta una linea capturando la salida y valida que no sea tecnica."""
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            continuar = ejecutar_linea(linea)
        texto = salida.getvalue()
        self.assertTrue(continuar, f"la linea corto el bucle: {linea!r}")
        self.assertNotIn("Traceback", texto)
        self.assertNotIn("Errno", texto)
        return texto

    def assertError(self, linea, fragmento=None):
        texto = self.ejecutar(linea)
        self.assertTrue(
            texto.startswith("[ERROR]"), f"salida inesperada: {texto!r}"
        )
        if fragmento is not None:
            self.assertIn(fragmento, texto)
        return texto

    def test_comando_mal_escrito_muestra_el_uso(self):
        self.assertError("crear editor cpu=8", "Uso: crear proceso")
        self.assertError("listar procesos extra", "sobra")
        self.assertError("volar proceso", "comando desconocido")
        self.assertError("archivo copiar notas.txt", "Uso: archivo")
        self.assertError("crear proceso @x cpu=1", "caracter no reconocido")

    def test_pid_inexistente(self):
        self.assertError("consultar proceso 99", "No existe el proceso 99")
        self.assertError("finalizar proceso 99", "No existe el proceso 99")
        self.assertError("memoria liberar 99", "no tiene memoria")
        self.assertEqual(procesos.listar_procesos(), [])

    def test_memoria_insuficiente(self):
        self.assertError(
            "crear proceso grande cpu=1 mem=2000", "memoria suficiente"
        )
        lista = procesos.listar_procesos()
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].estado.value, "RECHAZADO")
        self.assertEqual(memoria.estado_memoria().usada, 0)

        self.assertError("memoria asignar 1 2000", "capacidad total 1024 MB")
        self.assertEqual(memoria.estado_memoria().usada, 0)

    def test_ruta_con_punto_punto(self):
        self.assertError("archivo leer ../secreto.txt")
        self.assertError('archivo crear ../x.txt "x"')

        self.assertFalse((self.raiz / "secreto.txt").exists())
        self.assertFalse((self.raiz / "x.txt").exists())
        self.assertFalse((self.raiz / "carpeta_pruebas" / "secreto.txt").exists())

    def test_archivo_inexistente_y_duplicado(self):
        self.assertError("archivo leer falta.txt", "No existe el archivo")
        self.ejecutar('archivo crear notas.txt "hola"')
        self.assertError('archivo crear notas.txt "otra"', "Ya existe el archivo")

    def test_mensajes_y_estadisticas_sin_datos(self):
        self.assertError("mensaje recibir", "No hay mensajes")
        self.assertError("estadisticas", "Primero ejecuta")

    def test_el_bucle_continua_tras_un_error(self):
        self.assertError("consultar proceso 99")
        salida = self.ejecutar("ayuda planificar")
        self.assertIn("Round Robin", salida)


if __name__ == "__main__":
    unittest.main()
