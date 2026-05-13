## Arquitectura del repositorio

El repositorio conserva dos implementaciones del sistema:

- main: Es la versión actual basada en SQLite
- csv-version: Es la versión original basada en archivos CSV

La versión SQLite fue desarrollada tomando como base la arquitectura original del sistema CSV y posteriormente refactorizada para adaptar la persistencia y las pruebas unitarias.

## Comparación entre implementaciones

### Rama CSV
Persistencia basada en archivos:

```
 """
    Para interactuar con un archivo, para la persistencia de los datos, la primer
    funcionalidad a desarrollar será la lectura del fichero, para observar los 
    datos desde la terinal
    """
    with open(config.DATABASE_PATH, newline="\n",encoding="utf-8") as fichero:
        ## Definimos un nuevo lector, y establecemos el caracter ";" para separar los datos
        reader = csv.reader(fichero, delimiter=";")
        ## Recorremos los datos y extraemos los respectivos datos (DNI, nombre, apellido)
        for dni, nombre, apellido in reader:
            ## Creamos una instancia de la clase cliente con los respectivos datos
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)
```

### Rama main
Persistencia basada en una base de datos real:

```
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
```
## Cambios realizados durante la migración 

### Corrección de errores

Durante la migración de CSV a SQLite, se presentaron diversos errores al adaptar el código, que se fueron revisando durante este proceso.

En el módulo "database.py", que es el encargado de toda la funcionalidad de la base de datos se presentó lo siguiente:

### 1 - Problema: Uso de "DB" global

### Error: No such table

```
DB = "clientes.db"

class Clientes:

    @staticmethod
    def buscar(dni):
        with sqlite3.connect(DB) as conexion:  # ❌ usa variable global
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT dni, nombre, apellido FROM clientes WHERE dni = ?", (dni,)
            )
```
### Problema: 
Los tests usan "prueba.db", mientras que el código usa "clientes.db", dos bases de datos distintas, por lo que la tabla no existe

### Corregido

```
class Clientes:
    DB = "clientes.db"

    @staticmethod
    def buscar(dni):
        with sqlite3.connect(Clientes.DB) as conexion:  # ✔ consistente
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT dni, nombre, apellido FROM clientes WHERE dni = ?", (dni,)
            )
```

### 2 - Problema: Devolver tuplas

### Error: AtributeError "tuple" object has no atribute "dni"

```

fila = cursor.fetchone()
return fila

```

### Corregido

```

fila = cursor.fetchone()

if fila:
    return Cliente(*fila)  # ✔ conversión
return None

```

### 3 - Problema: Desempaquetar NONE

### Error: TypeError "NonType" object is no iterable

```

fila = cursor.fetchone()
return Cliente(*fila)  # ❌ falla si fila es None

```

### Corregido

```

fila = cursor.fetchone()

if fila:
    return Cliente(*fila)
return None

```

### 4 - Problema: INSERT sin parametrización clara

### Error: Confusión típica, faltaban parámetros

```

cursor.execute(
    "INSERT INTO clientes VALUES (?,?,?)"
)

```

### Corregido

```

cursor.execute(
    "INSERT INTO clientes (dni, nombre, apellido) VALUES (?, ?, ?)",
    (dni, nombre, apellido)
)

```

### 5 - Problema: modificar() sin validar existencia

### Error: Siempre devuleve algo aunque no exista

```

cursor.execute(
    "UPDATE clientes SET nombre = ?, apellido = ? WHERE dni = ?",
    (nombre, apellido, dni)
)
return Cliente(dni, nombre, apellido)

```

### Corregido

```

cliente = Clientes.buscar(dni)

if cliente:
    with sqlite3.connect(Clientes.DB) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE clientes SET nombre = ?, apellido = ? WHERE dni = ?",
            (nombre, apellido, dni)
        )
    return Cliente(dni, nombre, apellido)

return None

```

### 6 - Problema: borrar() no devolvia nada

### Error: AtributeError "NoneType" object has no atribute "dni"

```

@staticmethod
def borrar(dni):
    with sqlite3.connect(Clientes.DB) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM clientes WHERE dni = ?", (dni,)
        )
```

### Corregido

```

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

    return None

```

### 7 - Problema en tests: datos duplicados

### Se ejecuta varias veces, por lo que se duplican los datos

### Error: UNIQUE constraint failed 

```

cursor.executemany(
    "INSERT INTO clientes VALUES (?,?,?)", datos
)

```

### Corregido

```

cursor.execute("DELETE FROM clientes")

cursor.executemany(
    "INSERT INTO clientes VALUES (?,?,?)", datos
)

```

### 8 - Problema: Base de datos bloqueada

### Conexiones abiertas mucho tiempo

### Error: database is locked

```

self.conexion = sqlite3.connect("prueba.db")

```

### Corregido
### Conexión corta y controlada

```

with sqlite3.connect(db.Clientes.DB) as conexion:

```

### 9 - Problema: test de modificar mal diseñado
### No se validaba la base de datos

```

cliente_a_modificar = copy.copy(db.Clientes.buscar('28Z'))
cliente_modificado = db.Clientes.modificar('28Z', 'Mariana', 'García')

self.assertEqual(cliente_a_modificar.nombre, 'Ana')
self.assertEqual(cliente_modificado.nombre, 'Mariana')

```

### Corregido

```

cliente_original = db.Clientes.buscar('28Z')

db.Clientes.modificar('28Z', 'Mariana', 'García')
cliente_modificado = db.Clientes.buscar('28Z')

self.assertEqual(cliente_original.nombre, 'Ana')
self.assertEqual(cliente_modificado.nombre, 'Mariana')

```

### 10 - Problema: test de crear

```

self.assertEqual(len(db.Clientes.lista), 4)  # ❌ ya no existe lista

```

### Corregido

```

cliente = db.Clientes.buscar('39X')

self.assertIsNotNone(cliente)
self.assertEqual(cliente.dni, '39X')

```

### 11 - Problema: test de borrar
### Fallaba porque retornaba None

```

cliente_borrado = db.Clientes.borrar('48H')
self.assertEqual(cliente_borrado.dni, '48H')

```

### Corregido
### Método y test corregido

```

cliente_borrado = db.Clientes.borrar('48H')
cliente_eliminado = db.Clientes.buscar('48H')

self.assertEqual(cliente_borrado.dni, '48H')
self.assertIsNone(cliente_eliminado)

```
