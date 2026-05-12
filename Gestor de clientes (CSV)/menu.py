"""
Este menú servirá como alternativa a un entorno sin interfaz gráfica
"""

import os
import helpers
import database as db

## Definimos la función principal para el menú
def iniciar():
    while True:
        ## Limpiamos la pantalla con la función limpiar_pantalla 
        helpers.limpiar_pantalla()

        ## Mostramos por pantalla las opciones del menú
        print("======================  ")
        print(" Bienvenido al Gestor   ")
        print("======================  ")
        print("[1] Listar los clientes ")
        print("[2] Buscar un cliente   ")
        print("[3] Añadir un cliente   ")
        print("[4] Modificar un cliente")
        print("[5] Borrar un cliente   ")
        print("[6] Cerrar el gestor    ")
        print("======================  ")

        ## Leemos la opción seleccionada
        opcion = input("> ")

        ## Volvemos a limpiar la pantalla
        helpers.limpiar_pantalla()

        ## Desarrollamos la lógica del programa para cada opción
        if opcion == "1":
            ## Listamos los clientes registrado
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
        
        elif opcion == "2":
            ## Buscamos un cliente específico
            print("Buscando un cliente...\n")
            ## Llamamos a la función leer_texto y le definimos los parámetros
            dni = helpers.leer_texto(3,3,"DNI(2 int y un char)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado.")

        elif opcion == "3":
            ## Añadimos un cliente
            print("Añadiendo un cliente...\n")
            dni = None ## Establecemos el valor inicial del dni como vacío

            ## Este bucle se va a ejecutar hasta que el formato del DNI sea correcto
            while True:
                ## Leemos un dni
                dni = helpers.leer_texto(3,3,"DNI(2 int y un char)").upper()
                ## Comprobamos si cumple
                if helpers.dni_valido(dni,db.Clientes.lista):
                    break
            
            ## Leemos un nombre
            nombre = helpers.leer_texto(2,30,"Nombre(de 2 a 30 char)").capitalize()
            ## Leemos un apellido
            apellido = helpers.leer_texto(2,30,"Apellido(de 2 a 30 char)").capitalize()
            ## Creamos los clientes
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente")

        elif opcion == "4":
            ## Modificamos un cliente
            print("Modificando un cliente...\n")
            ## Leemos un dni
            dni = helpers.leer_texto(3,3,"DNI(2 int y un char)").upper()
            ## Buscamos al cliente a para verificar si existe
            cliente = db.Clientes.buscar(dni)
            
            ## Comprobamos si existe el cliente
            if cliente: ## Si no es None
                 ## Modificamos el nombre y mostramos el actual
                nombre = helpers.leer_texto(2,30,f"Nombre(de 2 a 30 char) [{cliente.nombre}]").capitalize()
                ## Modificamos el apellido y mostramos el actual
                apellido = helpers.leer_texto(2,30,f"Apellido(de 2 a 30 char) [{cliente.apellido}").capitalize()
                ## Una vez que hicimos lo anterior llamamos a la función modificar
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado correctamente...")
            
            else:
                print("Cliente no encontrado")


        elif opcion == "5":
            ## Borramos un cliente
            print("Borrando un cliente...\n")
            ## Buscamos un DNI
            dni = helpers.leer_texto(3,3,"DNI(2 int y un char)").upper()
            print("Cliente borrado correctamente.") if db.Clientes.borrar(dni) else print("Cliente no encontrado")
            

        elif opcion == "6":
            ## Salimos del programa
            print("Saliendo...\n")
            break

        input("\nPresiona ENTER para continuar...")