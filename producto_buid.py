from __future__ import annotations
from abc import ABC, abstractmethod

# Interfaz de que define los métodos para construir un producto generico

class IbuilderProducto(ABC):
    
    @abstractmethod
    def set_producto(self, nombre: str) -> IbuilderProducto:
        pass
    
    @abstractmethod
    def set_cantidad(self, cantidad: int) -> IbuilderProducto:
        pass
    
    @abstractmethod
    def set_precio(self, precio: float) -> IbuilderProducto:
        pass
    
    @abstractmethod
    def set_codigo(self, codigo: str) -> IbuilderProducto:
        pass
    
    @abstractmethod
    def build(self) -> dict:
        pass

# Contrutor concreto

class BuilderProducto(IbuilderProducto):
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.producto = {}
    
    def set_producto(self, nombre: str) -> BuilderProducto:
        self.producto['producto'] = nombre
        return self
    
    def set_cantidad(self, cantidad: int) -> BuilderProducto:
        self.producto['cantidad'] = cantidad
        return self
    
    def set_precio(self, precio: float) -> BuilderProducto:
        self.producto['precio'] = precio
        return self

    def set_codigo(self, codigo: str) -> BuilderProducto:
        self.producto['codigo'] = codigo
        return self

    def build(self):
        campo_requerido = ['producto', 'cantidad', 'precio', 'codigo']
        for campo in campo_requerido:
            if campo not in self.producto:
                raise ValueError(f"Falta el campo requerido: {campo}")
            

        producto_final = self.producto
        self.reset() 
        return producto_final    
