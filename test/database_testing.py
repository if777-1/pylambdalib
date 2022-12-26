import unittest
from redis import Redis
from pylambdalib.utils import get_connection

class TestDatabaseConnection(unittest.TestCase):

    def test_StrictRedis_db_with_correct_password(self):
        self.assertIsInstance(
            get_connection("localhost",6379),
            Redis,
            "La funcion get_connection debe devolver un objeto"
            "redis.StrictRedis al pasarle una contrasenia incorrecta")
    def test_keys_returns_list(self):
        self.assertIsInstance(
            get_connection("localhost",6379).keys('patron que no da nada'),
            list,
            "La funcion keys debe devolver una lista"
        )
    def test_get_returns_None_when_key_doesnt_exists(self):
        clave = "STRING DE PRUEBA PARA TESTEAR PYLAMBDALIB (CLAVE)"
        db = get_connection("localhost",6379)
        db.delete(clave)
        self.assertIsNone(
            db.get(clave),
            "La funcion get debe devolver un None si la clave no existe"
        )
    def test_get_returns_str_when_key_exists(self):
        db = get_connection("localhost",6379)
        clave = "STRING DE PRUEBA PARA TESTEAR PYLAMBDALIB (CLAVE)"
        valor = "STRING DE PRUEBA PARA TESTEAR PYLAMBDALIB (VALOR)"
        self.assertTrue(
            db.set(clave, valor),
            "Cualquier set debe dar True"
        )
        self.assertEqual(
            db.get(clave),
            valor,
            "La funcion get debe devolver el valor seteado"
        )
        self.assertTrue(
            db.delete(clave),
            "El delete debe dar True"
        )

if __name__ == "__main__":
    unittest.main()