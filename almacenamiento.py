import json as js
import os

class JsonUsuario:
    
    def __init__(self, archivo_json):
        self.archivo_json = archivo_json # Asigamos la ruta del archivo Json a un atributo
    
    def cargar_usuarios(self):
        """Si no existe, devuelve lista vacía."""
        if not os.path.exists(self.archivo_json):
            return []
        try:
            with open(self.archivo_json, "r") as archivo:
                return js.load(archivo)
        except js.JSONDecodeError:
            return []

    def guardar_usuarios(self, lista_usuarios):
        try:
            with open(self.archivo_json, "w") as archivo:
                js.dump(lista_usuarios, archivo, indent=4)
                return True
        except Exception as e:
            return False

class JsonInventario:
    def __init__(self, archivo_json):
        self.archivo_json = archivo_json

    def cargar_inventario(self):
        if not os.path.exists(self.archivo_json):
            return []
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as archivo:
                return js.load(archivo)
        except js.JSONDecodeError:
            return []

    def guardar_inventario(self, lista_inventario):
        try:
            with open(self.archivo_json, "w", encoding="utf-8") as archivo:
                js.dump(lista_inventario, archivo, indent=4, ensure_ascii=False)
                return True
        except Exception:
            return False