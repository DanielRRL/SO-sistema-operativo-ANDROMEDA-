import unittest

from lexer import tokenizar
from tokens import PALABRAS, RESERVADAS


def tipos(tokens):
    return [token.tipo for token in tokens]


class TestLexer(unittest.TestCase):
    def test_crear_proceso_completo(self):
        tokens = tokenizar("crear proceso editor llegada=0 cpu=8 prioridad=2 mem=128\n")
        self.assertEqual(
            tipos(tokens),
            [
                "CREAR",
                "PROCESO",
                "ID",
                "LLEGADA",
                "IGUAL",
                "NUMERO",
                "CPU",
                "IGUAL",
                "NUMERO",
                "PRIORIDAD",
                "IGUAL",
                "NUMERO",
                "MEM",
                "IGUAL",
                "NUMERO",
                "FIN",
            ],
        )
        self.assertEqual(tokens[2].lexema, "editor")
        self.assertEqual(tokens[2].linea, 1)
        self.assertEqual(tokens[2].columna, 15)

    def test_listar_procesos(self):
        self.assertEqual(tipos(tokenizar("listar procesos\n")), ["LISTAR", "PROCESOS", "FIN"])

    def test_consultar_proceso(self):
        self.assertEqual(
            tipos(tokenizar("consultar proceso 2")),
            ["CONSULTAR", "PROCESO", "NUMERO", "FIN"],
        )

    def test_finalizar_proceso(self):
        self.assertEqual(
            tipos(tokenizar("finalizar proceso 1")),
            ["FINALIZAR", "PROCESO", "NUMERO", "FIN"],
        )

    def test_planificar_con_quantum(self):
        self.assertEqual(
            tipos(tokenizar("planificar rr quantum=3")),
            ["PLANIFICAR", "RR", "QUANTUM", "IGUAL", "NUMERO", "FIN"],
        )

    def test_planificar_fcfs_y_sjf(self):
        self.assertEqual(tipos(tokenizar("planificar fcfs")), ["PLANIFICAR", "FCFS", "FIN"])
        self.assertEqual(tipos(tokenizar("planificar sjf")), ["PLANIFICAR", "SJF", "FIN"])

    def test_concurrencia_en_sus_tres_modos(self):
        for modo, tipo in (
            ("sin_lock", "SIN_LOCK"),
            ("con_lock", "CON_LOCK"),
            ("semaforo", "SEMAFORO"),
        ):
            with self.subTest(modo=modo):
                self.assertEqual(
                    tipos(tokenizar(f"concurrencia {modo}")),
                    ["CONCURRENCIA", tipo, "FIN"],
                )

    def test_memoria_estado_asignar_y_liberar(self):
        self.assertEqual(tipos(tokenizar("memoria estado")), ["MEMORIA", "ESTADO", "FIN"])
        self.assertEqual(
            tipos(tokenizar("memoria asignar 1 2000")),
            ["MEMORIA", "ASIGNAR", "NUMERO", "NUMERO", "FIN"],
        )
        self.assertEqual(
            tipos(tokenizar("memoria liberar 1")),
            ["MEMORIA", "LIBERAR", "NUMERO", "FIN"],
        )

    def test_archivo_crear_y_cadena(self):
        tokens = tokenizar('archivo crear notas.txt "hola mundo"\n')
        self.assertEqual(
            tipos(tokens),
            ["ARCHIVO", "CREAR", "NOMBRE_ARCHIVO", "CADENA", "FIN"],
        )
        self.assertEqual(tokens[2].lexema, "notas.txt")
        self.assertEqual(tokens[3].lexema, "hola mundo")

    def test_archivo_operaciones(self):
        self.assertEqual(tipos(tokenizar("archivo listar")), ["ARCHIVO", "LISTAR", "FIN"])
        self.assertEqual(
            tipos(tokenizar("archivo leer notas.txt")),
            ["ARCHIVO", "LEER", "NOMBRE_ARCHIVO", "FIN"],
        )
        self.assertEqual(
            tipos(tokenizar('archivo modificar notas.txt "nuevo"')),
            ["ARCHIVO", "MODIFICAR", "NOMBRE_ARCHIVO", "CADENA", "FIN"],
        )
        self.assertEqual(
            tipos(tokenizar("archivo eliminar notas.txt")),
            ["ARCHIVO", "ELIMINAR", "NOMBRE_ARCHIVO", "FIN"],
        )

    def test_mensajes(self):
        self.assertEqual(
            tipos(tokenizar('mensaje enviar "listo"')),
            ["MENSAJE", "ENVIAR", "CADENA", "FIN"],
        )
        self.assertEqual(
            tipos(tokenizar("mensaje recibir")),
            ["MENSAJE", "RECIBIR", "FIN"],
        )

    def test_utilidades(self):
        self.assertEqual(tipos(tokenizar("ejemplo")), ["EJEMPLO", "FIN"])
        self.assertEqual(tipos(tokenizar("ayuda planificar")), ["AYUDA", "PLANIFICAR", "FIN"])
        self.assertEqual(tipos(tokenizar("limpiar")), ["LIMPIAR", "FIN"])
        self.assertEqual(tipos(tokenizar("salir")), ["SALIR", "FIN"])

    def test_comando_tokens_reporta_error(self):
        tokens = tokenizar("tokens crear proceso @x")
        self.assertEqual(
            tipos(tokens),
            ["TOKENS", "CREAR", "PROCESO", "ERROR", "ID", "FIN"],
        )
        self.assertEqual(tokens[3].lexema, "@")
        self.assertEqual(tokens[3].columna, 22)

    def test_reservadas_mayusculas(self):
        tokens = tokenizar("CREAR PROCESO Editor CPU=8")
        self.assertEqual(
            tipos(tokens),
            ["CREAR", "PROCESO", "ID", "CPU", "IGUAL", "NUMERO", "FIN"],
        )
        self.assertEqual(tokens[2].lexema, "Editor")

    def test_todas_las_palabras_reservadas(self):
        self.assertEqual(len(PALABRAS), 36)
        for palabra, tipo in RESERVADAS.items():
            with self.subTest(palabra=palabra):
                tokens = tokenizar(palabra)
                self.assertEqual(tokens[0].tipo, tipo)
                self.assertEqual(tokens[-1].tipo, "FIN")

    def test_identificadores_y_nombres_de_archivo(self):
        tokens = tokenizar("notas.txt mi-archivo.txt editor")
        self.assertEqual(
            tipos(tokens),
            ["NOMBRE_ARCHIVO", "NOMBRE_ARCHIVO", "ID", "FIN"],
        )
        self.assertEqual(tokens[0].lexema, "notas.txt")
        self.assertEqual(tokens[1].lexema, "mi-archivo.txt")

    def test_nombre_reservado_no_es_identificador(self):
        self.assertEqual(tipos(tokenizar("cpu")), ["CPU", "FIN"])
        self.assertEqual(tipos(tokenizar("cpu8")), ["ID", "FIN"])

    def test_numero_y_igual(self):
        self.assertEqual(
            tipos(tokenizar("quantum=3")),
            ["QUANTUM", "IGUAL", "NUMERO", "FIN"],
        )

    def test_entrada_vacia(self):
        tokens = tokenizar("")
        self.assertEqual(tipos(tokens), ["FIN"])
        self.assertEqual(tokens[0].linea, 1)
        self.assertEqual(tokens[0].columna, 1)

    def test_linea_y_columna(self):
        tokens = tokenizar("crear proceso\neditor cpu=8")
        self.assertEqual(
            tipos(tokens),
            ["CREAR", "PROCESO", "ID", "CPU", "IGUAL", "NUMERO", "FIN"],
        )
        self.assertEqual((tokens[2].linea, tokens[2].columna), (2, 1))
        self.assertEqual((tokens[3].linea, tokens[3].columna), (2, 8))
        self.assertEqual((tokens[4].linea, tokens[4].columna), (2, 11))
        self.assertEqual((tokens[5].linea, tokens[5].columna), (2, 12))

    def test_comentarios(self):
        tokens = tokenizar("# comentario\ncrear proceso editor # fin\n")
        self.assertEqual(tipos(tokens), ["CREAR", "PROCESO", "ID", "FIN"])
        self.assertEqual((tokens[0].linea, tokens[0].columna), (2, 1))

    def test_hash_dentro_de_cadena(self):
        tokens = tokenizar('mensaje enviar "# no es comentario"')
        self.assertEqual(
            tipos(tokens),
            ["MENSAJE", "ENVIAR", "CADENA", "FIN"],
        )
        self.assertEqual(tokens[2].lexema, "# no es comentario")

    def test_cadena_con_escapes(self):
        tokens = tokenizar(r'mensaje enviar "hola \"mundo\"\n"')
        self.assertEqual(
            tipos(tokens),
            ["MENSAJE", "ENVIAR", "CADENA", "FIN"],
        )
        self.assertEqual(tokens[2].lexema, 'hola "mundo"\n')

    def test_cadena_sin_cerrar(self):
        tokens = tokenizar('mensaje enviar "sin cerrar')
        self.assertEqual(
            tipos(tokens),
            ["MENSAJE", "ENVIAR", "ERROR", "FIN"],
        )
        self.assertEqual(tokens[2].lexema, '"sin cerrar')
        self.assertEqual((tokens[2].linea, tokens[2].columna), (1, 16))

    def test_caracter_invalido_continua(self):
        tokens = tokenizar("crear proceso editor @")
        self.assertEqual(
            tipos(tokens),
            ["CREAR", "PROCESO", "ID", "ERROR", "FIN"],
        )
        self.assertEqual(tokens[3].lexema, "@")
        self.assertEqual(tokens[3].columna, 22)

    def test_salto_de_linea_crlf(self):
        tokens = tokenizar("crear proceso\r\neditor cpu=8")
        self.assertEqual(
            tipos(tokens),
            ["CREAR", "PROCESO", "ID", "CPU", "IGUAL", "NUMERO", "FIN"],
        )
        self.assertEqual((tokens[2].linea, tokens[2].columna), (2, 1))

    def test_tabulaciones(self):
        self.assertEqual(
            tipos(tokenizar("crear\tproceso")),
            ["CREAR", "PROCESO", "FIN"],
        )

    def test_archivo_que_empieza_con_numero(self):
        tokens = tokenizar("123.txt")
        self.assertEqual(tipos(tokens), ["NOMBRE_ARCHIVO", "FIN"])
        self.assertEqual(tokens[0].lexema, "123.txt")

    def test_matriz_de_25_casos_validos(self):
        casos_validos = [
            ("crear", "CREAR"),
            ("listar", "LISTAR"),
            ("consultar", "CONSULTAR"),
            ("finalizar", "FINALIZAR"),
            ("planificar", "PLANIFICAR"),
            ("estadisticas", "ESTADISTICAS"),
            ("concurrencia", "CONCURRENCIA"),
            ("mensaje", "MENSAJE"),
            ("memoria", "MEMORIA"),
            ("archivo", "ARCHIVO"),
            ("ejemplo", "EJEMPLO"),
            ("ayuda", "AYUDA"),
            ("tokens", "TOKENS"),
            ("limpiar", "LIMPIAR"),
            ("salir", "SALIR"),
            ("proceso", "PROCESO"),
            ("sin_lock", "SIN_LOCK"),
            ("MiProceso_2", "ID"),
            ("notas.txt", "NOMBRE_ARCHIVO"),
            ("123.log", "NOMBRE_ARCHIVO"),
            ("0", "NUMERO"),
            ("1024", "NUMERO"),
            ('"hola mundo"', "CADENA"),
            ("=", "IGUAL"),
            ("# comentario", "FIN"),
        ]
        self.assertGreaterEqual(len(casos_validos), 25)

        for entrada, tipo_esperado in casos_validos:
            with self.subTest(entrada=entrada):
                resultado = tokenizar(entrada)
                self.assertEqual(resultado[0].tipo, tipo_esperado)
                self.assertEqual(resultado[-1].tipo, "FIN")
                self.assertNotIn("ERROR", tipos(resultado))

    def test_matriz_de_25_casos_invalidos(self):
        caracteres_invalidos = [
            "@",
            "$",
            "%",
            "^",
            "&",
            "*",
            "+",
            "-",
            "/",
            "\\",
            ":",
            ";",
            "?",
            "!",
            "[",
            "]",
            "{",
            "}",
            "(",
            ")",
            ",",
            ".",
            "á",
            "ñ",
            "€",
        ]
        self.assertGreaterEqual(len(caracteres_invalidos), 25)

        for caracter in caracteres_invalidos:
            with self.subTest(caracter=caracter):
                resultado = tokenizar(f"crear {caracter}")
                self.assertIn("ERROR", tipos(resultado))
                self.assertEqual(resultado[-1].tipo, "FIN")

        for entrada in ('mensaje enviar "sin cerrar', 'mensaje enviar "corte\\'):
            with self.subTest(entrada=entrada):
                self.assertIn("ERROR", tipos(tokenizar(entrada)))


if __name__ == "__main__":
    unittest.main()
