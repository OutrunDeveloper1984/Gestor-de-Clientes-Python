"""
Este script contendrá funciones auxiliares 

"""
import re
import os

## Este módulo permite identificar el sistema operativo 
import platform

## Definimos la función limpiar_pantalla
def limpiar_pantalla():

    ## Comprobamos si el SO es windows
    if platform.system() == "Windows":
        os.system("cls")
    
    ## Para el caso de Mac o Linux
    else:
        os.system("clear")

"""
Esta función puede definirse tambien con un operador ternario, con la 
siguiente sintaxis

def limpiar_pantalla():
    os.system("cls") if platform.system() == "Windows" else os.system("clear")

"""
## Definimos la función leer_texto que recibe tres parámetros
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):

    ## Se muestra el mensaje en caso de que haya, en caso contrario no se hará nada
    print(mensaje) if mensaje else None
    while True:
        ## Se introducen datos
        texto = input("> ")
        ## Comprobamos si el texto ingresado cumple los requisitos
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto

## Esta función va a servir para verificar el DNI       
def dni_valido(dni,lista):
    ## Primero, si se cumple el formato establiecido para el DNI
    if not re.match("[0-9]{2}[A-Z]$",dni):
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    
    ## Validamos que no haya clientes con el DNI repetido
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI ocupado por otro cliente.")
            return False
    return True
