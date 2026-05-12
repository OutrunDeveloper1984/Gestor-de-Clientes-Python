"""
Este script no contendrá una base de datos como tal, sino que tendrá
control de estos 
"""

import csv
import config

##Creamos la clase cliente, para el manejo de estos
class Cliente:
    def __init__(self,dni,nombre,apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
    
    ## Definimos la función str, que dará estructura a la cadena que representa al cliente
    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"
    
## Esta clase permitirá gestionar el control
class Clientes:
    
    ## Lista de los clientes
    lista = []

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


    ## Definimos el método estático buscar un cliente, con el dni de este
    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente

    ## Definimos el método crear, con el dni, nombre y apellido como parámetros        
    @staticmethod
    def crear(dni,nombre,apellido):
        cliente = Cliente(dni, nombre, apellido)
        ## Lo agregamos a la lista de clientes
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente
    
     ## Definimos el método modificar, con el dni, nombre y apellido como parámetros     
    @staticmethod
    def modificar(dni, nombre, apellido):
        ## Necesitamos el indice y el objeto que estamos recorriendo
        for indice,cliente in enumerate(Clientes.lista):
            ## Comprobamos si los datos son los mismos, sino para modificar el nombre y el apellido
            if cliente.dni == dni:
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar()
                ## Devolvemos el objeto que se encuentra en dicha posición 
                return  Clientes.lista[indice]

    ## Definimos el método borrar para eliminar un cliente
    @staticmethod
    def borrar(dni):
        for indice,cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                ## Devolvemos al cliente borrado con el indice
                cliente = Clientes.lista.pop(indice)
                Clientes.guardar()
                return cliente
                          
    ## Definimos el método guardar, para almacenar los datos de un fichero
    @staticmethod
    def guardar():
        ## Abrimos el fichero en modo de escritura
        with open(config.DATABASE_PATH,"w",newline="\n",encoding="utf-8") as fichero:
            ## Definimos un writer para manejar los datos 
            writer = csv.writer(fichero, delimiter=";")
            for cliente in Clientes.lista:
                ## Llamamos al método writerow, y definimos los campos
                writer.writerow((cliente.dni, cliente.nombre, cliente.apellido))
                

