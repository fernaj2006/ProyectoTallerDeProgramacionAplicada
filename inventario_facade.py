from almacenamiento import JsonInventario
from inventario_logica import LogicaInventario
from strategy_reportes import EstrategiaReporte, ReporteTXT

class InventarioFacade:
    """Fachada del inventario.

    Patron estructural Facade: entrega una interfaz simple para que la vista
    trabaje con el inventario sin conocer los detalles de almacenamiento,
    validaciones ni creacion de productos con Builder.
    """

    def __init__(self, archivo_json='inventario.json'):
        almacenamiento = JsonInventario(archivo_json)
        self.logica = LogicaInventario(almacenamiento)

    def obtener_productos(self):
        return self.logica.obtener_inventario()

    def obtener_siguiente_codigo(self):
        return self.logica.generar_codigo()

    def crear_producto(self, nombre, cantidad_texto, precio_texto):
        es_valido, resultado = self._validar_datos_producto(nombre, cantidad_texto, precio_texto)
        if not es_valido:
            return False, resultado

        nombre_limpio, cantidad, precio = resultado
        self.logica.agregar_producto(nombre_limpio, cantidad, precio)
        return True, 'Producto agregado correctamente.'

    def actualizar_producto(self, codigo, nombre, cantidad_texto, precio_texto):
        es_valido, resultado = self._validar_datos_producto(nombre, cantidad_texto, precio_texto)
        if not es_valido:
            return False, resultado

        nombre_limpio, cantidad, precio = resultado
        actualizado = self.logica.actualizar_producto(codigo, nombre_limpio, cantidad, precio)
        if not actualizado:
            return False, 'No se encontro el producto seleccionado.'
        return True, 'Producto actualizado correctamente.'

    def eliminar_producto(self, codigo):
        self.logica.eliminar_producto(codigo)
        return True, 'Producto eliminado.'

    def buscar_productos(self, criterio):
        return self.logica.buscar_productos(criterio)

    def resetear_inventario(self):
        self.logica.resetear_inventario()
        return True, 'Inventario reseteado a valores originales.'

    def generar_reporte(self, estrategia: EstrategiaReporte = None, ruta_reporte='reporte_inventario.txt'):
        """Genera un reporte usando el patron Strategy.
 
        Args:
            estrategia: Objeto EstrategiaReporte (ReporteTXT o ReportePDF).
                        Si no se indica, usa ReporteTXT por defecto.
            ruta_reporte: Ruta del archivo de salida.
        """
        if estrategia is None:
            estrategia = ReporteTXT()  # comportamiento por defecto, sin romper nada
 
        contenido = estrategia.generar(self.logica.obtener_inventario())
 
        # PDF (fpdf2) retorna bytearray, TXT retorna str
        es_binario = isinstance(contenido, (bytes, bytearray))
        modo       = 'wb' if es_binario else 'w'
        encoding   = None if es_binario else 'utf-8'
 
        with open(ruta_reporte, modo, encoding=encoding) as archivo:
            archivo.write(contenido)
        return True, f'Reporte generado en {ruta_reporte}'
 
    def _validar_datos_producto(self, nombre, cantidad_texto, precio_texto):
        es_valido, mensaje = self.logica.validar_nombre_producto(nombre)
        if not es_valido:
            return False, mensaje

        es_valido, cantidad = self.logica.validar_cantidad(cantidad_texto)
        if not es_valido:
            return False, cantidad

        es_valido, precio = self.logica.validar_precio(precio_texto)
        if not es_valido:
            return False, precio

        return True, (nombre.strip(), cantidad, precio)
