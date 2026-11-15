"""Pruebas de la cola de mensajes (T3.10).

Se ejecutan con todas las demas desde la carpeta del proyecto:

    python3 -m unittest discover -s pruebas
"""
import threading
import unittest

import mensajes


class TestMensajes(unittest.TestCase):
    def setUp(self):
        mensajes.limpiar()          # cada prueba empieza con la cola vacia

    def test_cola_vacia(self):
        self.assertIsNone(mensajes.recibir())
        self.assertEqual(mensajes.cantidad(), 0)

    def test_enviar_y_recibir(self):
        mensajes.enviar("hola")
        self.assertEqual(mensajes.cantidad(), 1)
        self.assertEqual(mensajes.recibir(), "hola")
        self.assertEqual(mensajes.cantidad(), 0)

    def test_orden_fifo(self):
        for texto in ("uno", "dos", "tres"):
            mensajes.enviar(texto)
        self.assertEqual([mensajes.recibir() for _ in range(3)], ["uno", "dos", "tres"])

    def test_recibir_con_cola_vacia_despues_de_usarla(self):
        mensajes.enviar("a")
        mensajes.recibir()
        self.assertIsNone(mensajes.recibir())

    def test_limpiar(self):
        mensajes.enviar("a")
        mensajes.enviar("b")
        mensajes.limpiar()
        self.assertEqual(mensajes.cantidad(), 0)
        self.assertIsNone(mensajes.recibir())

    def test_texto_con_espacios_y_vacio(self):
        mensajes.enviar("hola mundo")
        mensajes.enviar("")
        self.assertEqual(mensajes.recibir(), "hola mundo")
        self.assertEqual(mensajes.recibir(), "")          # un texto vacio no es None
        self.assertIsNone(mensajes.recibir())

    def test_productor_y_consumidor_con_hilos(self):
        """Dos hilos productores y un consumidor: no se pierde ningun mensaje."""
        por_productor = 200
        recibidos = []

        def productor(nombre):
            for i in range(por_productor):
                mensajes.enviar(f"{nombre}-{i}")

        hilos = [threading.Thread(target=productor, args=(n,)) for n in ("p1", "p2")]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()

        while (m := mensajes.recibir()) is not None:
            recibidos.append(m)

        self.assertEqual(len(recibidos), 2 * por_productor)
        # Dentro de cada productor el orden se conserva (FIFO).
        for nombre in ("p1", "p2"):
            propios = [m for m in recibidos if m.startswith(nombre)]
            self.assertEqual(propios, [f"{nombre}-{i}" for i in range(por_productor)])


if __name__ == "__main__":
    unittest.main()