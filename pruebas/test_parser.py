"""Pruebas del parser (T3.9). Ejecutar desde la carpeta del proyecto:

    python pruebas/test_parser.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import tokenizar          # noqa: E402
from parser import ErrorSintaxis, Orden, parsear   # noqa: E402


def p(linea: str) -> Orden:
    return parsear(tokenizar(linea))


class OrdenesValidas(unittest.TestCase):
    def test_crear_completo(self):
        o = p("crear proceso editor llegada=0 cpu=8 prioridad=2 mem=128")
        self.assertEqual((o.comando, o.subcomando, o.argumentos), ("crear", "proceso", ("editor",)))
        self.assertEqual(o.atributos, {"llegada": 0, "cpu": 8, "prioridad": 2, "memoria": 128})

    def test_crear_solo_cpu_y_otro_orden(self):
        self.assertEqual(p("crear proceso a cpu=5").atributos, {"cpu": 5})
        self.assertEqual(p("crear proceso a mem=64 cpu=3").atributos, {"memoria": 64, "cpu": 3})

    def test_mayusculas(self):
        o = p("CREAR Proceso A CPU=5")
        self.assertEqual((o.comando, o.argumentos, o.atributos), ("crear", ("A",), {"cpu": 5}))

    def test_listar_consultar_finalizar(self):
        self.assertEqual(p("listar procesos").subcomando, "procesos")
        self.assertEqual(p("consultar proceso 2").argumentos, (2,))
        self.assertEqual(p("finalizar proceso 1").argumentos, (1,))

    def test_planificar(self):
        self.assertEqual((p("planificar fcfs").subcomando, p("planificar sjf").subcomando), ("fcfs", "sjf"))
        self.assertEqual(p("planificar rr").atributos, {"quantum": 3})
        self.assertEqual(p("planificar rr quantum=2").atributos, {"quantum": 2})

    def test_concurrencia(self):
        for modo in ("sin_lock", "con_lock", "semaforo"):
            self.assertEqual(p(f"concurrencia {modo}").subcomando, modo)

    def test_mensajes(self):
        self.assertEqual(p('mensaje enviar "hola mundo"').argumentos, ("hola mundo",))
        self.assertEqual(p("mensaje recibir").subcomando, "recibir")

    def test_memoria(self):
        self.assertEqual(p("memoria estado").subcomando, "estado")
        self.assertEqual(p("memoria").subcomando, "estado")
        self.assertEqual(p("memoria asignar 1 256").argumentos, (1, 256))
        self.assertEqual(p("memoria liberar 1").argumentos, (1,))

    def test_archivos(self):
        self.assertEqual(p('archivo crear notas.txt "hola"').argumentos, ("notas.txt", "hola"))
        self.assertEqual(p("archivo crear notas.txt").argumentos, ("notas.txt", ""))
        self.assertEqual(p("archivo listar").argumentos, ())
        self.assertEqual(p("archivo leer notas.txt").argumentos, ("notas.txt",))
        self.assertEqual(p('archivo modificar notas.txt "otra"').argumentos, ("notas.txt", "otra"))
        self.assertEqual(p("archivo eliminar notas.txt").argumentos, ("notas.txt",))

    def test_utilidades(self):
        for c in ("estadisticas", "ejemplo", "limpiar", "salir"):
            self.assertEqual(p(c).comando, c)
        self.assertEqual(p("ayuda").argumentos, ())
        self.assertEqual(p("ayuda planificar").argumentos, ("planificar",))

    def test_tokens_acepta_errores(self):
        self.assertEqual(p("tokens crear proceso @x").comando, "tokens")

    def test_linea_vacia_y_comentario(self):
        self.assertEqual(p("").comando, "")
        self.assertEqual(p("   ").comando, "")
        self.assertEqual(p("# solo un comentario").comando, "")


class Errores(unittest.TestCase):
    def assertError(self, linea, *fragmentos):
        with self.assertRaises(ErrorSintaxis) as cm:
            p(linea)
        for f in fragmentos:
            self.assertIn(f, str(cm.exception))

    def test_comando_desconocido(self):
        self.assertError("volar alto", "comando desconocido", "volar")

    def test_palabra_que_no_es_comando(self):
        self.assertError("cpu=8", "no es un comando")
        self.assertError("proceso 1", "no es un comando")

    def test_caracter_invalido_con_columna(self):
        self.assertError("crear proceso @x cpu=1", "'@'", "columna 15")

    def test_comilla_sin_cerrar(self):
        self.assertError('mensaje enviar "sin cerrar', "comilla sin cerrar")

    def test_crear_sin_proceso(self):
        self.assertError("crear editor cpu=8", "se esperaba 'proceso'", "Uso: crear proceso")

    def test_crear_sin_nombre(self):
        self.assertError("crear proceso", "falta el nombre")

    def test_crear_nombre_reservado(self):
        self.assertError("crear proceso cpu cpu=3", "palabra reservada")
        self.assertError("crear proceso salir cpu=3", "palabra reservada")

    def test_crear_nombre_invalido(self):
        self.assertError("crear proceso 123 cpu=3", "nombre de proceso invalido")

    def test_crear_atributo_repetido(self):
        self.assertError("crear proceso a cpu=3 cpu=4", "repetido")
        self.assertError("crear proceso a mem=3 mem=4 cpu=1", "repetido")

    def test_crear_falta_cpu(self):
        self.assertError("crear proceso a llegada=1", "falta el atributo cpu")

    def test_crear_cpu_cero(self):
        self.assertError("crear proceso a cpu=0", "al menos 1")

    def test_crear_falta_igual_o_valor(self):
        self.assertError("crear proceso a cpu 8", "falta '='")
        self.assertError("crear proceso a cpu=", "se esperaba un numero")

    def test_crear_atributo_desconocido(self):
        self.assertError("crear proceso a color=3", "se esperaba un atributo")

    def test_faltan_argumentos(self):
        self.assertError("consultar proceso", "se esperaba un numero", "Uso: consultar")
        self.assertError("listar", "se esperaba 'procesos'")
        self.assertError("memoria asignar 1", "se esperaba un numero")
        self.assertError("mensaje enviar", "texto entre comillas")

    def test_sobran_argumentos(self):
        self.assertError("salir ya", "sobra 'ya'")
        self.assertError("listar procesos extra", "sobra 'extra'")
        self.assertError("estadisticas 1", "sobra '1'")

    def test_rr_quantum_cero(self):
        self.assertError("planificar rr quantum=0", "al menos 1")

    def test_algoritmo_o_modo_invalido(self):
        self.assertError("planificar xyz", "se esperaba 'fcfs' o 'sjf' o 'rr'")
        self.assertError("concurrencia rapido", "se esperaba")

    def test_archivo_sin_extension_o_con_ruta(self):
        self.assertError("archivo leer notas", "con extension")
        self.assertError("archivo leer ../secreto.txt", "caracter no reconocido")

    def test_memoria_cero_mb(self):
        self.assertError("memoria asignar 1 0", "al menos 1")


class SesionDeDemo(unittest.TestCase):
    """Todas las lineas de pruebas/demo.txt deben parsear, salvo la que falla a proposito."""

    def test_demo(self):
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.txt")
        if not os.path.exists(ruta):
            self.skipTest("no existe pruebas/demo.txt")
        malas = []
        with open(ruta, encoding="utf-8-sig") as f:
            for linea in f:
                texto = linea.strip()
                if not texto or texto.startswith("#"):
                    continue
                try:
                    p(texto)
                except ErrorSintaxis:
                    malas.append(texto)
        self.assertEqual(malas, ["crear editor cpu=8"])   # el error de sintaxis a proposito


if __name__ == "__main__":
    unittest.main(verbosity=2)