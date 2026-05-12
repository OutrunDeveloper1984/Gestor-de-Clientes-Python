# Este fichero será para las pruebas unitarias

import unittest
import sqlite3
import os
import copy
import database as db
import helpers

class TestDatabase(unittest.TestCase):
    def setUp(self):

        # Creamos la base de datos de prueba
        db.Clientes.DB = "prueba.db"

        # Nos conectamos a la base de datos temporal
        self.conexion = sqlite3.connect(db.Clientes.DB)
        self.cursor = self.conexion.cursor()

        # Creamos la tabla
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                dni TEXT PRIMARY KEY,
                nombre VARCHAR(30) NOT NULL,
                apellido VARCHAR(30) NOT NULL                         
            )
        """)
        self.cursor.execute("DELETE FROM clientes")

        # Insertamos los datos de prueba
        datos = [
            ('15J','Marta','Pérez'),
            ('48H','Manolo','López'),
            ('28Z','Ana','García')
        ]

        # Agregamos los clientes
        self.cursor.executemany(
            "INSERT INTO clientes VALUES (?,?,?)", datos
        )
        self.conexion.commit()
    
    def tearDown(self):
        self.conexion.close()

    # Probamos la búsqueda de clientes
    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15J')
        cliente_inexistente = db.Clientes.buscar('99X')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
    
    # Probamos la creación de clientes
    def test_crear_cliente(self):
        db.Clientes.crear('39X','Héctor','Costa')
        cliente = db.Clientes.buscar('39X')
        
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.dni, '39X')
        self.assertEqual(cliente.nombre, 'Héctor')
        self.assertEqual(cliente.apellido, 'Costa')
    
    # Probamos modificar clientes
    def test_modificar_cliente(self):

        # Buscamos al cliente original con el DNI
        cliente_original = db.Clientes.buscar('28Z')

        # Hacemos el cambio
        db.Clientes.modificar('28Z', 'Mariana', 'García')

        # Verificamos el cambio
        cliente_modificado = db.Clientes.buscar('28Z')

        self.assertEqual(cliente_original.nombre, 'Ana')
        self.assertEqual(cliente_modificado.nombre, 'Mariana')
        self.assertEqual(cliente_modificado.apellido, 'García')

    # Probamos borrar un cliente
    def test_borrar_cliente(self):

        # Eliminamos el cliente
        cliente_borrado = db.Clientes.borrar('48H')

        # Buscamos el cliente
        cliente_eliminado = db.Clientes.buscar('48H')

        self.assertEqual(cliente_borrado.dni, '48H')
        self.assertIsNone(cliente_eliminado)
    
    # Probamos si el dni cumple con el formato
    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A'))
        self.assertFalse(helpers.dni_valido('232323'))
        self.assertFalse(helpers.dni_valido('F35'))
        
    
        
    
