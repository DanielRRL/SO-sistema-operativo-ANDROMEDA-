"""Pruebas de hilos_sync (T3.11)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hilos_sync import (  # noqa: E402
    MODOS,
    ResultadoConcurrencia,
    ejecutar_concurrencia,
    formatear_resultado,
)


class TestHilosSync(unittest.TestCase):
    def test_con_lock_es_correcto(self):
        r = ejecutar_concurrencia("con_lock", hilos=4, iteraciones=500)
        self.assertTrue(r.correcto)
        self.assertEqual(r.valor_obtenido, 2000)
        self.assertEqual(r.valor_esperado, 2000)

    def test_semaforo_es_correcto(self):
        r = ejecutar_concurrencia("semaforo", hilos=4, iteraciones=500)
        self.assertTrue(r.correcto)
        self.assertEqual(r.valor_obtenido, r.valor_esperado)

    def test_sin_lock_pierde_incrementos(self):
        r = ejecutar_concurrencia("sin_lock", hilos=4, iteraciones=2000)
        self.assertEqual(r.valor_esperado, 8000)
        self.assertLess(r.valor_obtenido, r.valor_esperado)
        self.assertFalse(r.correcto)

    def test_modo_en_mayusculas(self):
        self.assertEqual(ejecutar_concurrencia("CON_LOCK", 2, 10).modo, "con_lock")

    def test_modo_invalido(self):
        with self.assertRaises(ValueError):
            ejecutar_concurrencia("otro")

    def test_parametros_invalidos(self):
        with self.assertRaises(ValueError):
            ejecutar_concurrencia("con_lock", hilos=0)
        with self.assertRaises(ValueError):
            ejecutar_concurrencia("con_lock", iteraciones=0)

    def test_un_solo_hilo_sin_lock_es_correcto(self):
        self.assertTrue(ejecutar_concurrencia("sin_lock", hilos=1, iteraciones=100).correcto)

    def test_todos_los_modos_devuelven_resultado(self):
        for modo in MODOS:
            self.assertIsInstance(ejecutar_concurrencia(modo, 2, 50), ResultadoConcurrencia)

    def test_formato(self):
        txt = formatear_resultado(ejecutar_concurrencia("con_lock", 2, 10))
        self.assertTrue(txt.startswith("[OK]"))
        self.assertIn("Valor esperado: 20", txt)
        malo = ResultadoConcurrencia("sin_lock", 10, 7, False, "x")
        self.assertTrue(formatear_resultado(malo).startswith("[ERROR]"))


if __name__ == "__main__":
    unittest.main()
