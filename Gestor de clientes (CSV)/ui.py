"""
Este script servirá para hacer el menú del programa, pero en forma de
interfaz gráfica
"""

import helpers
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

class CenterWidgetMixin:
    ## Definimos el método center, para centrar la ventana principal de la GUI
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")

## Creamos una clase para la ventana de creación de cliente
class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.center()

        """
        Los dos métodos siguientes, hacen que la ventana de creación se bloquee
        y no permite interactuar con la ventana principal hasta que esta se cierre
        """
        self.transient(parent)
        self.grab_set()

    ## Definimos el método build para la interfaz de la ventana de creación
    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        ## Creamos las etiquetas para la información requerida
        Label(frame, text= "DNI (2 ints y 1 upper chart)").grid(row=0, column=0)
        Label(frame, text= "Nombre (2 a 30 char)").grid(row=0, column=1)
        Label(frame, text= "Apellido ( 2 a 30 char)").grid(row=0, column=2)

        ## Creamos los campos de texto (entrys)
        ## DNI
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))

        ## Nombre
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))

         ## Apellido
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady=10)

        ## Creamos el botón de creación
        crear = Button(frame, text="Crear", command=self.create_client)
        ## Configuramos al botón para que por defecto esté desactivado
        crear.configure(state=DISABLED)

        ## Indicamos que el botón se situe en la fila 0 y columna 0
        crear.grid(row=0, column=0)

        ## Creamos el boton de cancelar
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        ## Creamos la lista validaciones
        self.validaciones = [0,0,0]
        self.crear = crear

        ## Exportamos el dni, el nombre y el apellido
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    ## Definimos el método create_client, para crear el cliente
    def create_client(self):
        self.master.treeview.insert(
            parent="", index="end",iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        
        """
        Para sincronizar la función con los datos en la base de datos, hacemos referencia
        con la siguiente línea de código, y le pasamos como parámetros el DNI, el nombre
        y el apellido
        """
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())                    
        self.close()

    ## Definimos el método close para destruir la subventana
    def close(self):
        self.destroy()
        self.update()

    ## Definimos la función validate para la validación de los datos
    def validate(self, event, index):

        ## Recuperamos el valor del campo y lo guardamos en "valor"
        valor = event.widget.get()

        ## Empleamos operadores ternarios para la validación
        valido = helpers.dni_valido(valor,db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.config({"bg":"Green" if valido else "Red"})

        ## Cambiar el estado del botón con base a la validación
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED)

## Creamos la clase para modificar un cliente
class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    ## Definimos el método build para la interfaz de la ventana de creación
    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        ## Creamos las etiquetas para la información requerida
        Label(frame, text= "DNI (No se puede editar)").grid(row=0, column=0)
        Label(frame, text= "Nombre (2 a 30 char)").grid(row=0, column=1)
        Label(frame, text= "Apellido ( 2 a 30 char)").grid(row=0, column=2)

        ## Creamos los campos de texto (entrys)
        ## DNI
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        ##dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))

        """
        Dado que ya no se necesita validar el dato del DNI cuando editemos un cliente
        se comenta esta línea de código
        """
        ## Nombre
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))

         ## Apellido
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        """
        Queremos autocompletar los campos, y para hacer referencia al cliente seleccionado,
        tenemos que acceder al treeview de la ventana principal
        """
        cliente = self.master.treeview.focus() ## Recuperamos el cliente seleccionado
        campos = self.master.treeview.item(cliente,"values") ## Recuperamos sus datos

        ## Hacemos referencia a cada uno de los datos y empleamos el método insert
        dni.insert(0, campos[0])

        ## Desactivamos el campo del DNI para que no se pueda modificar
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        ## Creamos el botón de creación
        actualizar = Button(frame, text="Actualizar", command=self.edit_client)

        """
        Dado que en esta sección previamente se cargó ya el nombre, no se necesitará 
        deshalibitar el botón por defecto, también comentamos esta líne de código

        actualizar.configure(state=DISABLED)        
        """
        
        ## Indicamos que el botón se situe en la fila 0 y columna 0
        actualizar.grid(row=0, column=0)

        ## Creamos el boton de cancelar
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        ## En el caso de las validaciones serán true porque ya estarán validados los campos
        self.validaciones = [1,1]
        self.actualizar = actualizar

        ## Exportamos el dni, el nombre y el apellido
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    ## Definimos el método edit_client, para editar el cliente
    def edit_client(self):

        ## Recuperamos el cliente seleccionado
        cliente = self.master.treeview.focus()

        ## Especificamos el cliente seleccionado, y los datos a recuperar
        self.master.treeview.item(cliente, values=(self.dni.get(),self.nombre.get(),self.apellido.get()))

        """
        Sincronizamos la función con la base de datos 
        """
        db.Clientes.modificar(self.dni.get(),self.nombre.get(),self.apellido.get())
        self.close()

    ## Definimos el método close para destruir la subventana
    def close(self):
        self.destroy()
        self.update()

    ## Para la validación ya solo lo haremos con el nombre y el apellido
    def validate(self, event, index):

        ## Recuperamos el valor del campo y lo guardamos en "valor"
        valor = event.widget.get()

        ## Empleamos operadores ternarios para la validación
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.config({"bg":"Green" if valido else "Red"})

        ## Cambiar el estado del botón con base a la validación
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1,1] else DISABLED)



## Definimos la clase MainWindow que servirá como ventana principal
class MainWindow(Tk, CenterWidgetMixin): ## Heredamos de Tk y de la clase CenterWidgetMixin
    def __init__(self):
        ## Usamos super para llamar de la super clase TK el método init
        super().__init__()
        ## Definimos un título
        self.title("Gestor de clientes")
        ## Llamamos al metodo build
        self.build()
        self.center()

    ## Definimos al método build para la estructura 
    def build(self):
        frame = Frame(self)
        frame.pack()
    
        ## Este widget sirve para visualizar los datos como una tabla
        treeview = ttk.Treeview(frame)

        ## Configuramos las columnas con los datos
        treeview["column"] = ("DNI", "Nombre", "Apellido")

        """
        Configuramos el formato de las columnas
        """
        ## Para la primer columna, tamaño 0 y que no se estire, es decir, la ocultamos
        treeview.column("#0", width=0, stretch=NO)

        ## Centramos el título de cada columna
        treeview.column("DNI", anchor=CENTER) ## DNI
        treeview.column("Nombre", anchor=CENTER) ## Nombre
        treeview.column("Apellido", anchor=CENTER) ## Apellido

        ## Configuramos las cabeceras (lo que va a aparecer en cada columna)
        treeview.heading("DNI", text="DNI", anchor=CENTER) ## DNI
        treeview.heading("Nombre", text="Nombre", anchor=CENTER) ## Nombre
        treeview.heading("Apellido", text="Apellido", anchor=CENTER) ## Apellido

        ## Creamos un widget de scrollbar para navegar por los datos
        scrollbar = Scrollbar(frame) ## Se crea en el marco (frame)
        scrollbar.pack(side=RIGHT, fill=Y) ## En posición vertical

        treeview["yscrollcommand"] = scrollbar.set   

        for cliente in db.Clientes.lista:
            ## Para añadir un registro a la tabla
            treeview.insert(
                parent="", index="end",iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

        treeview.pack()

        ## Configuramos los botones de control para crear, modificar o borrar un registro
        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text="Crear", command=self.create).grid(row=0, column=0)
        Button(frame, text="Modificar", command=self.edit).grid(row=0, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2)

        ## Exportamos el widget treeview para tener acceso a el mediante otros métodos
        self.treeview = treeview

    ## Definimos el método delete
    def delete(self):
        """
        El método focus sirve para cuando seleccionamos un registro, pero este puede 
        devolver el registro, o también devuelve None, se hará una comprobación
        """
        cliente = self.treeview.focus()
        ## Comprobamos si se tiene seleccionado
        if cliente:
            ## Con el método item recuperamos el registro, y lo que queremos extraer
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title="Confirmar borrado",
                message=f"¿Borrar {campos[1]}{campos[2]}?",
                icon = WARNING
           )
            if confirmar:
                self.treeview.delete(cliente)

                """
                Para sincronizar la funcionalidad de la interfaz, con los datos de la base de datos
                hacemos referencia a ellos con la siguiente línea, y de los campos le pasamos como 
                argumento la primera posición (DNI)                
                """
                db.Clientes.borrar(campos[0])

    ## Definimos el método create, para crear un cliente
    def create(self):
        CreateClientWindow(self)

    ## Definimos el método edit, para modificar un cliente
    def edit(self):
        ## Comprobamos si hay un cliente seleccionado
        if self.treeview.focus():
            EditClientWindow(self)
  
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()