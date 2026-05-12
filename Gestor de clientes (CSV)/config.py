"""
Este fichero sirve para separar el archivo csv para realizar pruebas del
programa principal, de manera que cuando se ejecute las pruebas unitarias,
no haya problemas con modificaciones de los datos
"""

import sys

DATABASE_PATH = "clientes.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/clientes_test.csv"