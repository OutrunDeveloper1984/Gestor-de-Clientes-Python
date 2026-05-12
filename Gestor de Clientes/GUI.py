import helpers
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

class CenterWidgetMixin:
    # Método para centrar la ventana principal
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")

# Clase CreateClientWindow para la ventana de creación
class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.center()
        self.transient(parent)
        # Este método bloquea la ventana principal
        self.grab_set()
    
    # Método build para crear un cliente
    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Etiquetas del título
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (De 2 a 30 char)").grid(row=0, column=1)
        Label(frame, text="Apellido (De 2 a 30 char)").grid(row=0, column=2)

        # Campos de texto "Entrys"

        # Entry para el DNI
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))

        # Entry para el nombre
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        # Entry para el apellido
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        #  Frame para separar
        frame = Frame(self)
        frame.pack(pady=10)

        # Agregamos el botón de crear
        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [0, 0, 0]
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    # Para crear un nuevo cliente (guardar el registro)
    def create_client(self):
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())) 
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get()) # Creamos el registro en la base de datos
        self.close()

    def close(self):
        self.destroy()
        self.update()
    
    def validate(self, event, index):
        valor = event.widget.get()

        # Validamos el DNI
        if index == 0:

            # Primero validamos que el formato es correcto
            valido = helpers.dni_valido(valor)

            if valido:
                
                # Verificamos si el DNI ya existe
                existe, mensaje = db.Clientes.dni_existe(valor)

                # Si ya existe
                if existe:
                    print(mensaje)

                    event.widget.configure({"bg":"Orange"})

                    self.validaciones[index] = False
                
                # Si no existe
                else:
                    event.widget.configure({"bg":"Green"})

                    self.validaciones[index] = True

            else:
                event.widget.configure({"bg":"Red"})

                self.validaciones[index] = False
        
        # Validamos el nombre y apellido
        if index == 1 or index == 2:

            valido = valor.isalpha() and 2 <= len(valor) <= 30

            event.widget.configure({
                "bg": "Green" if valido else "Red"
            })

            # cambiamos el estado del botón con base en las validaciones
            self.validaciones[index] = valido
            self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

# Clase EditClientWindow para la ventana de edición
class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.center()
        self.transient(parent)
        # Este método bloquea la ventana principal
        self.grab_set()
    
    # Método build para crear un cliente
    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Etiquetas del título
        Label(frame, text="DNI (No editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (De 2 a 30 char)").grid(row=0, column=1)
        Label(frame, text="Apellido (De 2 a 30 char)").grid(row=0, column=2)

        # Campos de texto "Entrys"

        # Entry para el DNI
        dni = Entry(frame)
        dni.grid(row=1, column=0)

        # Entry para el nombre
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))

        # Entry para el apellido
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        # Recuperamos el cliente seleccionado en el treeview
        cliente = self.master.treeview.focus()

        # Extraemos los valores
        campos = self.master.treeview.item(cliente, 'values')

        # Hacemos la referencia a cada campo de texto
        dni.insert(0, campos[0])
        dni.config(state=DISABLED) # Desactivamos el DNI para que no se pueda editar
        nombre.insert(1, campos[1])
        apellido.insert(2, campos[2])

        #  Frame para separar
        frame = Frame(self)
        frame.pack(pady=10)

        # Agregamos el botón de actualizar
        actualizar = Button(frame, text="Actualizar", command=self.edit_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [1, 1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    # Para actualizar un registro
    def edit_client(self):

        # Recuperamos el cliente seleccionado
        cliente = self.master.treeview.focus()
        
        # Indicamos cuales son los valores que queremos recuperar de los campos de nombre y apellido
        self.master.treeview.item(cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()
    
    def validate(self, event, index):
        valor = event.widget.get()
        
        # Validamos solo el nombre y apellido
        if index == 0 or index == 1:

            valido = valor.isalpha() and 2 <= len(valor) <= 30

            event.widget.configure({
                "bg": "Green" if valido else "Red"
            })

            # cambiamos el estado del botón con base en las validaciones
            self.validaciones[index] = valido
            self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)
           
           
# Definimos la clase para la ventana principal
class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Clientes")
        self.build()
        self.center()

    # Método para definir la estructura de la interfaz
    def build(self):
        frame = Frame(self)
        frame.pack()

        # El widget treeview sirve para darnos una vista en árbol (es la vista principal en tabla de la GUI)
        treeview = ttk.Treeview(frame)
        treeview['column'] = ('DNI', 'Nombre', 'Apellido')
        

        # Ocultamos la primera columna
        treeview.column("#0",width=0, stretch=NO)

        # Centramos el DNI, el Nombre y el Apellido
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        # Configuramos el formato de las cabeceras
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        # Para la barra de scroll o scrollbar
        scrollbar = Scrollbar(frame)

        # La empaquetamos al lado derecho y lo rellene verticalmente
        scrollbar.pack(side=RIGHT, fill=Y)

        # Indicamos al treeview que use la scrollbar
        treeview['yscrollcommand'] = scrollbar.set

        # Para insertar un cliente
        for cliente in db.Clientes.listar():
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        # Para crear los botones
        Button(frame, text="Crear", command=self.create).grid(row=0, column=0)
        Button(frame, text="Modificar", command=self.edit).grid(row=0, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2)

        # Exportamos el widget treeview para acceder a sus métodos
        self.treeview = treeview
    
    # Método delete para eliminar un cliente
    def delete(self):

        # Usamos "focus" para el cliente seleccionado
        cliente = self.treeview.focus()

        # Verificamos si hay algo en lugar de None
        if cliente:
            campos = self.treeview.item(cliente, 'values')
            confirmar = askokcancel(
            title="Confirmar borrado",
            message=f"¿Borrar {campos[1]} {campos[2]}?",
            icon=WARNING
            )
            if confirmar:
                self.treeview.delete(cliente) # Borramos el registro de la tabla
                db.Clientes.borrar(campos[0]) # Borramos el registro de la base de datos

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        # Nos aseguramos que haya un cliente seleccionado
        if self.treeview.focus():
            EditClientWindow(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()