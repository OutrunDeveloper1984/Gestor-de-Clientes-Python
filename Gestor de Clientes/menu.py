## Este Script tendrá la esctructura del menú principal

import os
import helpers
import database as db

# Función principal del menú
def iniciar():
    while True:

        # Limpiando la pantalla con limpiar_pantalla
        helpers.limpiar_pantalla()

        # Mostrando las opciones del menú
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

        # Leyendo la opción
        opcion = input("> ")

        # Nuevamente limpiamos la pantalla
        helpers.limpiar_pantalla()

        # Desarrollamos la lógica del programa para cada opción
        if opcion == '1':
            print("Listando los clientes...\n")
            clientes = db.Clientes.listar()

            if not clientes:
                print("No hay clientes registrados")
            else:
                for cliente in clientes:
                    print(f"DNI: {cliente.dni} | Nombre: {cliente.nombre} | Apellido: {cliente.apellido}")

        # Opción para buscar a los clientes
        if opcion == '2':
            print("Buscando un cliente...\n")

            # Verificamos el DNI
            dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            
            # Mostramos un mensaje de que si existe o no el cliente
            print(cliente) if cliente else print("Cliente no encontrado.")

        # Opción para agregar un cliente
        if opcion == '3':
            print("Añadiendo un cliente...\n")

            while True:
                # Validamos que el DNI cumpla con el formato definido
                dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper()

                # Si el formato falla se mostrará un mensaje de error
                if helpers.dni_valido(dni):
                    break
                else:
                    print("Formato de DNI inválido")

            # Si la condición anterior se cumple se verifica el nombre y el apellido
            nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 char)").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 char)").capitalize()

            # Creamos el cliente
            if db.Clientes.crear(dni, nombre, apellido):
                print("Cliente añadido correctamente.")
            else:
                print("Error: El DNI ya está registrado")

        # Opción para modificar un cliente
        if opcion == '4':
            print("Modificando un cliente...\n")

            # Validamos el DNI del cliente a modificar
            dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper()

            # Buscamos el cliente
            cliente = db.Clientes.buscar(dni)

            # Verificamos si existe el cliente
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"Nombre (de 2 a 30 char) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido (de 2 a 30 char) [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, cliente.nombre, cliente.apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado.")

        # Opción para borrar un cliente
        if opcion == '5':
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 int y 1 char)").upper()

            # Verificamos si existe el cliente
            print("Cliente borrado correctamente.") if db.Clientes.borrar(dni) else print("Cliente no encontrado.")

        if opcion == '6':
            print("Saliendo...\n")
            break

        input("\nPresiona ENTER para continuar...")