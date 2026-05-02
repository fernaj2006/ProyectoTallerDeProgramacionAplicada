import tkinter as tk
from tkinter import messagebox

class LogicaUsuarios:
    
    def __init__(self, almacenamiento):
        self.almacenamiento = almacenamiento #asignamos el archivo almacenamiento en un atributo
    
    def registrar_usuario(self, nuevo_usuario):
        
        # Cargamos los usuarios existentes
        usuarios = self.almacenamiento.cargar_usuarios()
        
        # Verificamos si el nombre de usuario ya existe
        for u in usuarios:
            if u['username'] == nuevo_usuario['username']:
                return False 
        
        # Agregamos el nuevo usuario
        usuarios.append(nuevo_usuario)
        
        # Guardamos la lista actualizada
        self.almacenamiento.guardar_usuarios(usuarios)
        return True
        
    def validar_acceso(self, usuario_ingresado):
        
        # Cargamos los usuarios existentes
        usuarios = self.almacenamiento.cargar_usuarios()
        
        # Bucle que recorre la lista para comparar los usarios ingresados con los existentes
        for u in usuarios:
            if u['username'] == usuario_ingresado['username'] and u['password'] == usuario_ingresado['password']:
                return True
        return False