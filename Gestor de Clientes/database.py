import sqlite3


## Clase cliente para definir la estructura que deberá tener un objeto cliente
class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    ## Función que devuelve la representación de la cadena de texto en caso de consulta
    def __str__(self):
        return f"({self.dni} {self.nombre} {self.apellido})"
    
# Clase clientes que gestiona a los clientes y funcionará como un módulo
class Clientes:

    # Creamos la base de datos "Clientes.db"
    DB = "clientes.db"

    #Inicializamos la tabla
    def crear_tabla():
        conexion = sqlite3.connect(Clientes.DB)
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            dni TEXT NOT NULL UNIQUE PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            apellido VARCHAR(30) NOT NULL                         
        )
        """)
        conexion.commit()
        conexion.close()


    # Método de búsqueda
    @staticmethod
    def buscar(dni):
        with sqlite3.connect(Clientes.DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT dni, nombre, apellido FROM clientes WHERE dni = ?", (dni,)
            )
            fila = cursor.fetchone()
            if fila:
                return Cliente(*fila)
            return None

    # Método de creación
    @staticmethod
    def crear(dni, nombre, apellido):
        try:
            with sqlite3.connect(Clientes.DB) as conexion:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "INSERT INTO clientes (dni, nombre, apellido) VALUES (?,?,?)", (dni, nombre, apellido)
                    )
            return True
        except sqlite3.IntegrityError:
            return False             

    # Método de modificación
    @staticmethod
    def modificar(dni, nombre, apellido):
        with sqlite3.connect(Clientes.DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE clientes SET nombre = ?, apellido = ? WHERE dni = ?",(nombre, apellido, dni)
            )
    
    # Método de borrado
    @staticmethod
    def borrar(dni):
        cliente = Clientes.buscar(dni)

        if cliente:
            with sqlite3.connect(Clientes.DB) as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "DELETE FROM clientes WHERE dni = ?", (dni,)
                )
        return cliente
        
    
    # Método de listado
    @staticmethod
    def listar():
        with sqlite3.connect(Clientes.DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM clientes"
            )
            filas = cursor.fetchall()
            if not filas:
                return []
            return [Cliente(*fila) for fila in filas]
        
    # Método que valida si ya existe un DNI
    @staticmethod
    def dni_existe(dni):

        with sqlite3.connect(Clientes.DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT dni FROM clientes WHERE dni = ?", (dni,)
            )
            resultado = cursor.fetchone()
            if resultado:
                return True, "El DNI ya existe"
            return False, ""
    