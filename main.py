import tkinter as tk
import re
import pygubu
from tkinter import messagebox, simpledialog
from almacenamiento import JsonUsuario, JsonInventario
from login_logica import LogicaUsuarios
from inventario_logica import LogicaInventario

class InterfazLogin:
    """Vista del login: muestra el formulario de acceso y registro."""

    def __init__(self, controlador_logica):
        self.builder = pygubu.Builder()
        self.logica = controlador_logica

        # Carga la interfaz desde el archivo XML de PyGubu
        self.builder.add_from_file('login.ui')
        self.main_window = self.builder.get_object('ventana_principal')

        # Configuración de pantalla de registro secundaria
        self.ventana_reg = self.builder.get_object('ventana_registro')
        self.ventana_reg.withdraw()

        # Conectar botones al controlador de eventos
        btn_ingresar = self.builder.get_object('btn_ingresar')
        btn_ingresar.configure(command=self.iniciar_sesion)

        btn_abrir_reg = self.builder.get_object('btn_abrir_registro')
        btn_abrir_reg.configure(command=self.mostrar_ventana_registro)

        btn_cerrar_reg = self.builder.get_object('btn_volver')
        btn_cerrar_reg.configure(command=self.cerrar_ventana_registro)

        btn_guardar = self.builder.get_object('btn_guardar_registro')
        btn_guardar.configure(command=self.registrar_usuario)

        self.ventana_reg.protocol("WM_DELETE_WINDOW", self.cerrar_todo)

    def iniciar(self):
        self.main_window.mainloop()

    def iniciar_sesion(self):
        usuario_ingresado = self.builder.get_object('login_usuario').get().strip()
        password_ingresada = self.builder.get_object('login_pass').get().strip()

        if not usuario_ingresado or not password_ingresada:
            messagebox.showwarning("Atención", "Por favor, ingresa tu usuario y contraseña.")
            return

        credenciales = {'username': usuario_ingresado, 'password': password_ingresada}
        acceso_concedido = self.logica.validar_acceso(credenciales)

        if acceso_concedido:
            messagebox.showinfo("Bienvenido", f"¡Acceso concedido, {usuario_ingresado}!")

            try:
                if self.ventana_reg.winfo_exists():
                    self.ventana_reg.destroy()
            except Exception:
                pass
            
            self.main_window.withdraw()

            inventario_json = JsonInventario('inventario.json')
            logica_inventario = LogicaInventario(inventario_json)
            sistema_almacen = SistemaAlmacenamiento(logica_inventario, self)
            sistema_almacen.iniciar()
            
            # Cuando se cierra la ventana de almacenamiento, volver a mostrar el login
            self.main_window.deiconify()
            self.builder.get_object('login_usuario').delete(0, tk.END)
            self.builder.get_object('login_pass').delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def mostrar_ventana_registro(self):
        self.ventana_reg.deiconify()
        self.main_window.withdraw()

    def cerrar_ventana_registro(self):
        self.ventana_reg.withdraw()
        self.main_window.deiconify()

    def registrar_usuario(self):
        username = self.builder.get_object('reg_usuario').get()
        password = self.builder.get_object('reg_password').get()

        nuevo_usuario = {'username': username, 'password': password}

        patrones_permitidos = r'^[a-zA-Z0-9._\s-]+$'
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return
        if not re.match(patrones_permitidos, username):
            messagebox.showerror("Error", "El usuario contiene caracteres no válidos.")
            return
        if username[0] == " " or username[-1] == " ":
            messagebox.showerror("Error", "El usuario no puede contener un espacio vacio al principio ni al final")
            return
        if username[0] == "_" or username[-1] == "_":
            messagebox.showerror("Error", "El usuario no puede comenzar y terminar con '_'.")
            return
        if not username.isdigit() == False:
            messagebox.showerror("Error", "El usuario no puede contener solo numeros.")
            return
        if username[0].isdigit():
            messagebox.showerror("Error", "El usuario no puede empezar con numeros.")
            return

        registro_exitoso = self.logica.registrar_usuario(nuevo_usuario)
        if registro_exitoso:
            messagebox.showinfo("Registro", "Usuario registrado con éxito")
            self.builder.get_object('reg_usuario').delete(0, tk.END)
            self.builder.get_object('reg_password').delete(0, tk.END)
            self.cerrar_ventana_registro()
        else:
            messagebox.showerror("Error", "Ese nombre de usuario ya está en uso. Elige otro.")

    def cerrar_todo(self):
        self.ventana_reg.destroy()
        self.main_window.destroy()

class SistemaAlmacenamiento:
    """Vista del inventario: muestra los productos y delega acciones al controlador."""

    def __init__(self, logica_inventario, interfaz_login=None):
        self.logica = logica_inventario
        self.interfaz_login = interfaz_login
        self.builder = pygubu.Builder()
        self.builder.add_from_file('sistema_almacenamiento.ui')
        self.main_window = self.builder.get_object('ventana_principal')
        self.treeview = self.builder.get_object('treeview_excel')

        self.btn_crear = self.builder.get_object('btn_crear')
        self.btn_actualizar = self.builder.get_object('btn_actualizar')
        self.btn_eliminar = self.builder.get_object('btn_eliminar')
        self.btn_buscar = self.builder.get_object('btn_buscar')
        self.btn_reporte = self.builder.get_object('btn_reporte')

        self.btn_crear.configure(command=self.mostrar_crear_producto)
        self.btn_actualizar.configure(command=self.mostrar_actualizar_producto)
        self.btn_eliminar.configure(command=self.mostrar_eliminar_producto)
        self.btn_buscar.configure(command=self.mostrar_buscar_producto)
        self.btn_reporte.configure(command=self.mostrar_reporte)

        frame_inferior = self.builder.get_object('frame_inferior')
        self.btn_reset = tk.Button(frame_inferior, text='Resetear Inventario', background='#e67e22', foreground='#ffffff', command=self.mostrar_resetear)
        self.btn_reset.pack(side='left', padx=10)
        
        self.btn_cerrar_sesion = tk.Button(frame_inferior, text='Cerrar Sesión', background='#e74c3c', foreground='#ffffff', command=self.cerrar_sesion)
        self.btn_cerrar_sesion.pack(side='right', padx=10)

        self.configurar_treeview()
        self.actualizar_vista()

        self.main_window.update_idletasks()
        ancho = self.main_window.winfo_reqwidth()
        alto = self.main_window.winfo_reqheight()
        self.main_window.geometry(f"{ancho}x{alto}")

        # Configurar el manejador para cuando se cierre la ventana
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_cerrar_ventana)

    def on_cerrar_ventana(self):
        """Maneja el cierre de la ventana de almacenamiento."""
        self.main_window.destroy()

    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login."""
        self.main_window.quit()
        self.main_window.destroy()

    def iniciar(self):
        self.main_window.mainloop()

    def configurar_treeview(self):
        self.treeview['columns'] = ('codigo', 'producto', 'cantidad', 'precio')
        self.treeview['show'] = 'headings'
        self.treeview.heading('codigo', text='Código')
        self.treeview.heading('producto', text='Producto')
        self.treeview.heading('cantidad', text='Cantidad')
        self.treeview.heading('precio', text='Precio')
        self.treeview.column('codigo', width=120, anchor='center')
        self.treeview.column('producto', width=450, anchor='w')
        self.treeview.column('cantidad', width=120, anchor='center')
        self.treeview.column('precio', width=120, anchor='center')

    def actualizar_vista(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for item in self.logica.obtener_inventario():
            self.treeview.insert('', 'end', values=(
                item.get('codigo', ''),
                item.get('producto', ''),
                item.get('cantidad', ''),
                item.get('precio', '')
            ))

    def mostrar_crear_producto(self):
        dialog = tk.Toplevel(self.main_window)
        dialog.title('Crear nuevo producto')
        dialog.transient(self.main_window)
        dialog.resizable(False, False)
        dialog.grab_set()

        codigo_auto = self.logica.generar_codigo()

        tk.Label(dialog, text='Código (Auto):').grid(row=0, column=0, sticky='e', padx=8, pady=8)
        tk.Label(dialog, text=codigo_auto, fg='blue', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=8, pady=8, sticky='w')

        tk.Label(dialog, text='Producto:').grid(row=1, column=0, sticky='e', padx=8, pady=8)
        entry_producto = tk.Entry(dialog, width=25)
        entry_producto.grid(row=1, column=1, padx=8, pady=8)

        tk.Label(dialog, text='Cantidad:').grid(row=2, column=0, sticky='e', padx=8, pady=8)
        entry_cantidad = tk.Entry(dialog, width=25)
        entry_cantidad.grid(row=2, column=1, padx=8, pady=8)

        tk.Label(dialog, text='Precio:').grid(row=3, column=0, sticky='e', padx=8, pady=8)
        entry_precio = tk.Entry(dialog, width=25)
        entry_precio.grid(row=3, column=1, padx=8, pady=8)

        def on_aceptar():
            producto = entry_producto.get()
            cantidad_text = entry_cantidad.get()
            precio_text = entry_precio.get()

            es_valido, error_msg = self.logica.validar_nombre_producto(producto)
            if not es_valido:
                messagebox.showerror('Error de validación', error_msg, parent=dialog)
                return

            es_valido, cantidad = self.logica.validar_cantidad(cantidad_text)
            if not es_valido:
                messagebox.showerror('Error de validación', cantidad, parent=dialog)
                return

            es_valido, precio = self.logica.validar_precio(precio_text)
            if not es_valido:
                messagebox.showerror('Error de validación', precio, parent=dialog)
                return

            self.logica.agregar_producto(producto.strip(), cantidad, precio)
            self.actualizar_vista()
            messagebox.showinfo('Inventario', 'Producto agregado correctamente.', parent=self.main_window)
            dialog.destroy()

        tk.Button(dialog, text='Aceptar', command=on_aceptar, width=10).grid(row=4, column=0, padx=8, pady=12)
        tk.Button(dialog, text='Cancelar', command=dialog.destroy, width=10).grid(row=4, column=1, padx=8, pady=12)

    def mostrar_actualizar_producto(self):
        seleccionado = self.treeview.selection()
        if not seleccionado:
            messagebox.showwarning('Advertencia', 'Selecciona un registro para actualizar.', parent=self.main_window)
            return

        item_id = seleccionado[0]
        valores = self.treeview.item(item_id, 'values')
        codigo_actual = valores[0]
        producto_actual = valores[1]
        cantidad_actual = valores[2]
        precio_actual = valores[3]

        dialog = tk.Toplevel(self.main_window)
        dialog.title('Actualizar producto')
        dialog.transient(self.main_window)
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text='Código:').grid(row=0, column=0, sticky='e', padx=8, pady=8)
        tk.Label(dialog, text=codigo_actual, fg='blue', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=8, pady=8, sticky='w')

        tk.Label(dialog, text='Producto:').grid(row=1, column=0, sticky='e', padx=8, pady=8)
        entry_producto = tk.Entry(dialog, width=25)
        entry_producto.insert(0, producto_actual)
        entry_producto.grid(row=1, column=1, padx=8, pady=8)

        tk.Label(dialog, text='Cantidad:').grid(row=2, column=0, sticky='e', padx=8, pady=8)
        entry_cantidad = tk.Entry(dialog, width=25)
        entry_cantidad.insert(0, cantidad_actual)
        entry_cantidad.grid(row=2, column=1, padx=8, pady=8)

        tk.Label(dialog, text='Precio:').grid(row=3, column=0, sticky='e', padx=8, pady=8)
        entry_precio = tk.Entry(dialog, width=25)
        entry_precio.insert(0, precio_actual)
        entry_precio.grid(row=3, column=1, padx=8, pady=8)

        def on_actualizar():
            producto = entry_producto.get()
            cantidad_text = entry_cantidad.get()
            precio_text = entry_precio.get()

            es_valido, error_msg = self.logica.validar_nombre_producto(producto)
            if not es_valido:
                messagebox.showerror('Error de validación', error_msg, parent=dialog)
                return

            es_valido, cantidad = self.logica.validar_cantidad(cantidad_text)
            if not es_valido:
                messagebox.showerror('Error de validación', cantidad, parent=dialog)
                return

            es_valido, precio = self.logica.validar_precio(precio_text)
            if not es_valido:
                messagebox.showerror('Error de validación', precio, parent=dialog)
                return

            self.logica.actualizar_producto(codigo_actual, producto.strip(), cantidad, precio)
            self.actualizar_vista()
            messagebox.showinfo('Inventario', 'Producto actualizado correctamente.', parent=self.main_window)
            dialog.destroy()

        tk.Button(dialog, text='Actualizar', command=on_actualizar, width=10).grid(row=4, column=0, padx=8, pady=12)
        tk.Button(dialog, text='Cancelar', command=dialog.destroy, width=10).grid(row=4, column=1, padx=8, pady=12)

    def mostrar_eliminar_producto(self):
        seleccionado = self.treeview.selection()
        if not seleccionado:
            messagebox.showwarning('Advertencia', 'Selecciona un registro para eliminar.', parent=self.main_window)
            return
        if not messagebox.askyesno('Confirmar', '¿Eliminar el producto seleccionado?', parent=self.main_window):
            return

        item_id = seleccionado[0]
        codigo = self.treeview.item(item_id, 'values')[0]
        self.logica.eliminar_producto(codigo)
        self.actualizar_vista()
        messagebox.showinfo('Inventario', 'Producto eliminado.', parent=self.main_window)

    def mostrar_buscar_producto(self):
        criterio = simpledialog.askstring('Buscar', 'Buscar por código o producto:', parent=self.main_window)
        if criterio is None:
            return

        resultados = self.logica.buscar_productos(criterio)
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for item in resultados:
            self.treeview.insert('', 'end', values=(
                item.get('codigo', ''),
                item.get('producto', ''),
                item.get('cantidad', ''),
                item.get('precio', '')
            ))
        if not resultados:
            messagebox.showinfo('Buscar', 'No se encontraron productos con ese criterio.', parent=self.main_window)

    def mostrar_reporte(self):
        ruta_reporte = 'reporte_inventario.txt'
        contenido = self.logica.generar_reporte()
        with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        messagebox.showinfo('Reporte', f'Reporte generado en {ruta_reporte}', parent=self.main_window)

    def mostrar_resetear(self):
        if not messagebox.askyesno('Confirmar', '¿Resetear el inventario a los valores originales? Esto eliminará todos los cambios.', parent=self.main_window):
            return
        self.logica.resetear_inventario()
        self.actualizar_vista()
        messagebox.showinfo('Inventario', 'Inventario reseteado a valores originales.', parent=self.main_window)

if __name__ == '__main__':
    direccion_json = JsonUsuario('usuarios.json')
    controlador_logica = LogicaUsuarios(direccion_json)
    app = InterfazLogin(controlador_logica)
    app.iniciar()
