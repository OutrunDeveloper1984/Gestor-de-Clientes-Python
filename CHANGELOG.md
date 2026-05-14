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

### Corrección de errores módulo database y test_database

Durante la migración de CSV a SQLite, se presentaron diversos errores al adaptar el código, que se fueron revisando durante este proceso.

El módulo "database.py" que es el encargado de la funcionalidad de la base de datos, y el módulo "test_database.py", encargado de realizar las pruebas unitarias para verificar la integridad de las funciones, se presentaron los siguientes errores:

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

### Corrección de errores módulo menu y database

El módulo "menu", es el que se encarga de presentar las diferentes opciones con las que cuenta la aplicación del gestor de clientes, así como de presentarlas en el modo terminal, este consiste en llamadas a la bases de datos, por lo que la integración entre los dos módulos, así como la inicialización de la base de datos, también presentó diferentes errores que se revisaron conforme se presentaron:

### 1 - Problema: no such table clientes

La tabla clientes nunca había sido creada antes de ejecutar consultas como:

```

cursor.execute("SELECT * FROM clientes")

```

SQLite crea automaticamente el archivo ".db", pero no crea tablas de forma automática

### 2 - Creación explícita de la tabla 
Cuando se iniciaba el programa, la tabla no se creaba

```

menu.iniciar()

```

Por lo que se agregó una inicialización explícita antes de iniciar el menu

```

db.Clientes.inicializar()
menu.iniciar()

```

### 3 - Unificación de la base de datos

Existian dos nombres diferentes:

```
DB = "clientes.db"
```
y

```
DB = "Clientes.db"
```

Lo que provocaba creación de múltiples archivos ".db", tablas inexistentes en una de las bases de datos y un comportamiento inconsistente

```

DB = "clientes.db"

class Clientes:
    DB = "Clientes.db"

```

Unificación a una sola base de datos

```

class Clientes:
    DB = "clientes.db"

```

### 4 - Centralización de la lógica de la base de datos

La función de creación de la tabla estaba fuera de la clase "Clientes"

```

def crear_tabla():
    conexion = sqlite3.connect(DB)

```

La inicialización se introdujo dentro de la clase "Clientes"

```

class Clientes:

    DB = "clientes.db"

    @staticmethod
    def inicializar():
        with sqlite3.connect(Clientes.DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    dni TEXT PRIMARY KEY,
                    nombre VARCHAR(30) NOT NULL,
                    apellido VARCHAR(30) NOT NULL
                )
            """)

```

### 5 - Corrección del método listar()

Se llamó al mismo método dentro sí mismo:

```
cliente = Clientes.listar()
```

Lo que generó un error de recursión "RecursionError: maximum recursion depth exceeded", porque se llamaba a si mismo infinitamente

### 6 - Corrección de la recursión
Antes

```

@staticmethod
def listar():
    cliente = Clientes.listar()

    if cliente:
        ...

```

Después: Se eliminó la llamada recursiva, y se consultó directamente a la base de datos

```

@staticmethod
def listar():
    with sqlite3.connect(Clientes.DB) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT dni, nombre, apellido FROM clientes"
        )
        filas = cursor.fetchall()

        return [Cliente(*fila) for fila in filas]

```

### 7 - Conversión de tuplas SQLite a objetos "cliente"
SQLite devolvía tuplas

```

[
    ('123', 'Oscar', 'Gonzalez')
]

```

Ahora cada fila se convierte en un objeto "Cliente"

```
return [Cliente(*fila) for fila in filas]
```

ya que la línea

`Cliente(*fila)` Equivale a `Cliente(fila[0], fila[1], fila[2])`

### 8 - Manejo correcto de listas vacías
Antes no había control cuando no había clientes

Después, el menú verifica si la lista está vacía

```

clientes = db.Clientes.listar()

if not clientes:
    print("No hay clientes registrados.")

```

Explicación del `if not clientes`:

Python interpreta `[]` como `False`, por eso: `if not clientes:` significa `if clientes está vacío`

Con lo anteriormente mencionado, se obtuvieron los siguientes resultados:

- Se utiliza solo una base de datos SQLite
- Se mantiene la persistencia entre las ejecuciones
- Se crea la tabla automaticamente si esta no existe
- Devuleven objetos `Cliente` correctamente
- Manejo de listas vacias sin errores
- Se evita la recursión accidental
- Centralización de toda la lógica de base de datos dentro de la clase `Clientes`

### Módulo helpers y validaciones en formato

El módulo "helpers", está dedicado a funciones auxiliares, donde una de estas, verifica que se cumpla el formato del DNI, además de que en esta etapa, también se verificaron otras validaciones, así como el manejo de registros duplicados, una mejora del flujo de interacción del usuario.

Durante esta etapa del proyecto se realizaron ajustes principalmente en:

- Validaciones del DNI
- Manejo de duplicados
- Conexión entre el menú y la base de datos
- Adaptación de pruebas unitarias
- Mejora del flujo de interacción del usuario

### 1 - Separación de responsabilidades en la validación del DNI

Originalmente, una sola función se encargaba de:

- Validar el formato
- Verificar duplicados

```

def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato")
        return False

    for cliente in lista:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente")
            return False

    return True

```
Esto presentó varios errores, como lo fueron:

- Mezcla de validaciones de formato
- Lógica de persistencia
- Manejo de datos almacenados

### 2 - Refactorización de la validación de formato

La validación del formato se aisló como función auxiliar independiente

```

import re

def validar_dni_formato(dni):
    return re.match(r'^[0-9]{2}[A-Z]$', dni) is not None

```
Tuvo mejoras en:

- Es una función mas simple
- Reutilizable
- Más fácil de probar
- Es independiente de la base de datos

### 3 - Manejo de duplicados dentro de `database.py`

La comprobación de DNI duplicado dejó de hacerse manualmente y pasó a manejarse directamente en la isnerción del cliente

Antes:

```

cursor.execute(
    "INSERT INTO clientes (dni, nombre, apellido) VALUES (?,?,?)",
    (dni, nombre, apellido)
)

```

Problema:

Si el DNI ya existía, SQLite lanzaba una excepción, y el flujo podía romperse

Después:

```

@staticmethod
def crear(dni, nombre, apellido):
    try:
        with sqlite3.connect(Clientes.DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO clientes (dni, nombre, apellido) VALUES (?,?,?)",
                (dni, nombre, apellido)
            )
        return True

    except sqlite3.IntegrityError:
        return False

```

Mejoras:

- Manejo de errores
- La función informa si la operación fue exitosa
- Se evita que el programa se detenga por excepciones

### 4 - Integración correcta con el menú principal

El menú pasó de asumir que todo salió bien, a verificar el resultado de la inserción

Antes:

```

db.Clientes.crear(dni, nombre, apellido)
print("Cliente añadido correctamente.")

```
Problema:

El mensaje de éxito aparecía incluso si el DNI ya existía

Después:

```

if db.Clientes.crear(dni, nombre, apellido):
    print("Cliente añadido correctamente.")
else:
    print("Error: el DNI ya está registrado.")

```
Mejoras:

- Mensajes coherentes con el resultado real
- Mejor manejo de errores
- Separación entre lógica y presentación

### 5 - Mejora en la validación interactiva del DNI

Se añadió un ciclo para repetir la entrada del DNI hasta que el formato sea válido

Antes:

Si el DNI era inválido, el flujo regresaba al menú principal

Después:

```

while True:
    dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper()

    if helpers.validar_dni_formato(dni):
        break

    print("Formato inválido")

```

Mejoras:

- Mejor experiencia de usuario
- Evita reiniciar toda la operación
- Flujo más natural

### 6 - Adaptación de pruebas unitarias

Las pruebas dejaron de validar múltiples responsabilidades juntas

Antes:

```

self.assertFalse(helpers.dni_valido('48H'))

```

Problema: La prueba asumía que la función también verificaba duplicados

### 7 - Separación de pruebas por responsabilidad 

Validación de formato

```

def test_dni_formato_valido(self):
    self.assertTrue(helpers.validar_dni_formato('00A'))

```

```

def test_dni_formato_invalido(self):
    self.assertFalse(helpers.validar_dni_formato('123'))

```

Validación de duplicados

```

def test_dni_duplicado(self):
    db.Clientes.crear('48H', 'Juan', 'Perez')

    self.assertFalse(
        db.Clientes.crear('48H', 'Otro', 'Nombre')
    )

```

Mejoras:

- Tests más claros
- Responsabilidades separadas
- Mejor mantenimiento

### 8 - Corrección del retorno en la función de validación

Problema detectado

La función devolvía `None` en casos válidos:

```

def dni_valido(dni):
    if not re.match(...):
        return False

```
Provocaba el error: `AssertionError: None is not true`

Solución aplicada:

```

def validar_dni_formato(dni):
    return re.match(r'^[0-9]{2}[A-Z]$', dni) is not None

```
Mejoras:

- La función siempre devuelve `True` o `False`
- Los tests funcionan correctamente

