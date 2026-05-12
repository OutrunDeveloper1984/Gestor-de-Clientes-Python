"""
Este será el archivo principal, que hará correr a todo el programa

"""
import ui
import sys
import menu

## Comprobamos si el script se ejecuta como programa principal
if __name__ == "__main__":

    """
    Nota importante: Si bien el programa se creo con una interfaz gráfica y un menú principal,
    este archivo, como ya se indica será el principal, por lo que antes de todo, se deberá 
    iniciar este script, ya que con este, se identifica si se requiere trabajar tanto en modo
    terminal, como de manera gráfica (Con la UI), de manera que en la sección de abajo, se hace
    la comprobación, con un argumento par indicar al sistema, que modalidad es requerida, aunque 
    de manera independiente, el script ui.py, se puede correr directamente
    
    """
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.iniciar()
    else:
        app = ui.MainWindow()
        app.mainloop()

