# Script con funciones auxiliares

# Importamos los módulos necesarios
import os

# Importamos el módulo platform para identificar el SO
import platform

# Importamos el módulo re para expresiones regulares
import re

# Definimos la función limpiar_pantalla
def limpiar_pantalla():

    # Si el sistema operativo es Windows
    if platform.system() == "Windows":
        os.system("cls")
    
    # Si es Mac O Linux
    else:
        os.system("clear")

# Esta función servirá para leer el texto ingresado
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        
# Esta función servirá para validar el DNI
def dni_valido(dni):
    # Si no cumple el formato se muestra un mensaje de error
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato")
        return False
    return True
    