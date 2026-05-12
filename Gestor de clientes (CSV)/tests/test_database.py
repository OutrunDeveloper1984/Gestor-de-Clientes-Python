"""
Este script sirve para probar las funcionalidades del módulo database

"""
## Importamos los respectivos módulos
import copy
import unittest
import database as db
import helpers
import config
import csv

## Creamos la clase TestDatabase
class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente("15J","Martha","Pérez"),
            db.Cliente("48H","Manolo","López"),
            db.Cliente("28Z","Ana","García")
        ]
    
    ## Definimos la función test_buscar_cliente para probar la función buscar
    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar("15J")
        cliente_inexistente = db.Clientes.buscar("99X")
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    ## Definimos la función test_crear_cliente para probar la función crear
    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear("39X","Héctor","Costa")
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni,"39X")
        self.assertEqual(nuevo_cliente.nombre,"Héctor")
        self.assertEqual(nuevo_cliente.apellido,"Costa")

    ## Definimos la función test_modificar_cliente para probar la función modificar
    def test_modificar_cliente(self):
        ## Hacemos una copia del cliente buscado con "copy"
        cliente_a_modificar = copy.copy(db.Clientes.buscar("28Z"))
        cliente_modificado = db.Clientes.modificar("28Z","Mariana","García")
        self.assertEqual(cliente_a_modificar.nombre,"Ana")
        self.assertEqual(cliente_modificado.nombre,"Mariana")

    ## Definimos la función test_borrar_cliente para probar la función borrar
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar("48H")
        cliente_rebuscado = db.Clientes.buscar("48H")
        self.assertEqual(cliente_borrado.dni,"48H")
        self.assertIsNone(cliente_rebuscado)

    ## Definimos la función test_DNI, para validar este parámetro 
    def test_DNI(self):
        self.assertTrue(helpers.dni_valido("00A", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("232323S", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("F35", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("48H", db.Clientes.lista))

    ## Definimos una función para comprobar que los datos si se estén almacenando en el fichero
    def test_escritura_csv(self):
        db.Clientes.borrar("48H")
        db.Clientes.borrar("15J")
        db.Clientes.modificar("28Z", "Mariana","García")

        ## Definimos tres variables
        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline="\n", encoding="utf-8") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            dni, nombre, apellido = next(reader)
        
        self.assertEqual(dni, "28Z")
        self.assertEqual(nombre, "Mariana")
        self.assertEqual(apellido, "García")