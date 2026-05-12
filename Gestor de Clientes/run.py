import GUI
import sys
import menu
import database as db

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        db.Clientes.crear_tabla()
        menu.iniciar()
    else:
        app = GUI.MainWindow()
        app.mainloop()
