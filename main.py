import tkinter as tk
import re
import pygubu
from tkinter import messagebox
from almacenamiento import JsonUsuario
from login_logica import LogicaUsuarios

class InterfazLogin:
    
    def __init__(self, controlador_logica):
  
        self.builder = pygubu.Builder() # Constructor de la clase InterfazLogin
        self.logica = controlador_logica # Asignamos el controlador lógico inyectado al atrtbuto de la clase
        
        #Carga el archivo visual (login.ui)
        self.builder.add_from_file('login.ui')

        #Obtiene la ventana principal (Login)
        self.main_window = self.builder.get_object('ventana_principal')
        
        #Obtiene la ventana de registro y la oculta para que no aparezca al ejecutar
        self.ventana_reg = self.builder.get_object('ventana_registro')
        self.ventana_reg.withdraw()
        
        #########################################
        #               Botones                 #
        #########################################
        
        #Obtemos el boton ingresar y llamamos al metodo validar_acceso al hacer click
        btn_ingresar = self.builder.get_object('btn_ingresar')
        btn_ingresar.configure(command=self.iniciar_sesion)
        
        #Obtemos el boton registro y llamamos al metodo mostrar_ventana_registro al hacer click
        btn_abrir_reg = self.builder.get_object('btn_abrir_registro')
        btn_abrir_reg.configure(command=self.mostrar_ventana_registro)
        
        #Obtemos el boton volver y llamamos al metodo cerrar_ventana_registro al hacer click
        btn_cerrar_reg = self.builder.get_object('btn_volver')
        btn_cerrar_reg.configure(command=self.cerrar_ventana_registro)
        
        #Obtemos el boton guardar y llamamos al metodo registrar_usuario al hacer click
        btn_guardar = self.builder.get_object('btn_guardar_registro')
        btn_guardar.configure(command=self.registrar_usuario)
        
        self.ventana_reg.protocol("WM_DELETE_WINDOW", self.cerrar_todo) # termina la aplicación al cerrar la ventana de registro

    #########################################
    #               Metodos                 #
    #########################################

    def iniciar(self):
        self.main_window.mainloop() # Bucle de la aplicación
        
    def iniciar_sesion(self):
        
        # Obtenemos los datos de la pantalla de Login y limpiamos espacios
        usuario_ingresado = self.builder.get_object('login_usuario').get().strip()
        password_ingresada = self.builder.get_object('login_pass').get().strip()
        
        # Verificamos que no esten vacios las entradas de usuario y contraseña
        if not usuario_ingresado or not password_ingresada:
            messagebox.showwarning("Atención", "Por favor, ingresa tu usuario y contraseña.")
            return
            
        # Armamos el diccionario para mandarlo a la lógica
        credenciales = {
            'username': usuario_ingresado,
            'password': password_ingresada
        }
        
        # Le preguntamos a login_logica.py si los datos son correctos
        acceso_concedido = self.logica.validar_acceso(credenciales)
        
        if acceso_concedido:
            messagebox.showinfo("Bienvenido", f"¡Acceso concedido, {usuario_ingresado}!\n\nSirviendo el plato fuerte...")
            
            # Limpiamos las entradas de texto 
            self.builder.get_object('login_usuario').delete(0, tk.END)
            self.builder.get_object('login_pass').delete(0, tk.END)
            
            # AQUÍ ES DONDE CONECTAS EL PLATO FUERTE
            # self.main_window.destroy() <-- Cerraría el login
            # abrir_ventana_principal_de_tu_app() <-- Abriría tu programa real   
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        
    def mostrar_ventana_registro(self):
        self.ventana_reg.deiconify() # Muestra la ventana de registro 
        self.main_window.withdraw() # Oculta la ventana de login
        
    def cerrar_ventana_registro(self):
        self.ventana_reg.withdraw()  # Cierra la ventana de registro
        self.main_window.deiconify() # Muestra la ventana de login
        
    def registrar_usuario(self):
        
        # Obtenemos los datos ingresados en los campos de texto de la ventana de registro
        username = self.builder.get_object('reg_usuario').get()
        password = self.builder.get_object('reg_password').get()
        
        # Creamos un diccionario
        nuevo_usuario = {
            'username': username,
            'password': password
        }
        
        ###### Validaciones de registro ######
        
        patrones_permitidos = r'^[a-zA-Z0-9._\s-]+$'
        
        #Validamos que los campos no estén vacíos
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return
        
        #Validamos que solo sean simbolos permitidos
        if not re.match(patrones_permitidos, username):
            messagebox.showerror("Error", "El usuario contiene caracteres no válidos.")
            return
        
        #Validamos que no comienze con un espacio en vacio
        if username[0] == " " or username[-1] == " ":
            messagebox.showerror("Error", "El usuario no puede contener un espacio vacio al principio ni al final")
            return 
        
        #Validamos que no comienze ni termine con el "_"
        if username[0] == "_" or username[-1] == "_":
            messagebox.showerror("Error", "El usuario no puede comenzar y terminar con '_'.")
            return 
        
        #Validamos que no sea puros numeros
        if not username.isdigit() == False:
            messagebox.showerror("Error", "El usuario no puede contener solo numeros.")
            return 
        
        #Validamos que no empieze con un numero
        if username[0].isdigit():
            messagebox.showerror("Error", "El usuario no puede empezar con numeros.")
            return 
        
        ###### Fin validaciones ######
        
        registro_exitoso = self.logica.registrar_usuario(nuevo_usuario) # llamamos al metodo registrar_usuario de login_logica.py, devuelve un boolenao 
        
        if registro_exitoso:
            messagebox.showinfo("Registro", "Usuario registrado con éxito")
            # Limpiamos los campos
            self.builder.get_object('reg_usuario').delete(0, tk.END)
            self.builder.get_object('reg_password').delete(0, tk.END)
            
            self.cerrar_ventana_registro() # Volvemos a la ventana principal
        else:
            messagebox.showerror("Error", "Ese nombre de usuario ya está en uso. Elige otro.")

    def cerrar_todo(self): 
        self.ventana_reg.destroy() # Cierra ambas ventanas
        self.main_window.destroy() # termina la aplicación

if __name__ == '__main__':
    direccion_json = JsonUsuario('usuarios.json') # Le pasamos la ruta del archivo Json al constructor de JsonUsarios 
    controlador_logica = LogicaUsuarios(direccion_json) # Pasamos el gestor al contructor de logica de usuarios
    app = InterfazLogin(controlador_logica) # Pasamos el controlador lógico al constructor de la interfaz gráfica
    app.iniciar() # llamamos al metodo iniciar para que comience a funcionar el bucle