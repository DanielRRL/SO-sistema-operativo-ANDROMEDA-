import unittest

from lexer import tokenizar


class TestLexer(unittest.TestCase):
    def test_tokeniza_comando_valido(self):
        tokens = tokenizar('crear editor 0 5 2 128\n')
        self.assertEqual(tokens[0].tipo, 'CREAR')
        self.assertEqual(tokens[1].tipo, 'ID')
        self.assertEqual(tokens[2].tipo, 'NUMERO')
        self.assertEqual(tokens[3].tipo, 'NUMERO')
        self.assertEqual(tokens[4].tipo, 'NUMERO')
        self.assertEqual(tokens[5].tipo, 'NUMERO')

    def test_tokeniza_cadena_y_archivo(self):
        tokens = tokenizar('archivo crear nota.txt "hola mundo"\n')
        self.assertEqual(tokens[0].tipo, 'ARCHIVO')
        self.assertEqual(tokens[1].tipo, 'CREAR')
        self.assertEqual(tokens[2].tipo, 'ID')
        self.assertEqual(tokens[3].tipo, 'CADENA')

    def test_tokeniza_comando_planificar(self):
        tokens = tokenizar('planificar rr 2\n')
        self.assertEqual(tokens[0].tipo, 'PLANIFICAR')
        self.assertEqual(tokens[1].tipo, 'RR')
        self.assertEqual(tokens[2].tipo, 'NUMERO')

    def test_rechaza_caracter_invalido(self):
        with self.assertRaises(ValueError):
            tokenizar('crear editor $ 0 5 2 128\n')


if __name__ == '__main__':
    unittest.main()
