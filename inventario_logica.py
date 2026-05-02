class LogicaInventario:
    """Controlador: Lógica de negocio del inventario (Principio DIP y SRP).
    
    Esta clase contiene toda la lógica de validación y manipulación del inventario.
    Cumple con el patrón MVC como controlador y aplica los principios SOLID:
    - SRP: Solo responsable de la lógica del inventario
    - DIP: Recibe inyección de dependencias (almacenamiento)
    """
    
    def __init__(self, almacenamiento):
        """Inicializa el controlador con inyección de dependencias.
        
        Args:
            almacenamiento: Objeto que implementa cargar_inventario() y guardar_inventario()
        """
        self.almacenamiento = almacenamiento
        self.lista_inventario = []
        self.cargar()

    def cargar(self):
        """Carga el inventario del almacenamiento (JSON)."""
        self.lista_inventario = self.almacenamiento.cargar_inventario()
        if not self.lista_inventario:
            # Si está vacío, carga valores por defecto
            self.lista_inventario = self._inventario_por_defecto()
            self.almacenamiento.guardar_inventario(self.lista_inventario)

    def obtener_inventario(self):
        """Retorna el inventario actual (lista de productos)."""
        return self.lista_inventario

    def generar_codigo(self):
        """Genera automáticamente el siguiente código basado en los existentes.
        
        Busca el código numérico más alto y suma 1, con formato de 3 dígitos (001, 002, etc.)
        """
        codigos_numericos = []
        for item in self.lista_inventario:
            try:
                num = int(item['codigo'])
                codigos_numericos.append(num)
            except ValueError:
                # Ignora códigos no numéricos
                pass
        siguiente = max(codigos_numericos) + 1 if codigos_numericos else 1
        return str(siguiente).zfill(3)

    def validar_nombre_producto(self, nombre):
        """Valida que el nombre del producto sea válido.
        
        Validaciones:
        - No puede estar vacío
        - No puede contener números
        - No puede contener signos especiales
        
        Returns:
            Tupla (es_valido: bool, mensaje_error: str)
        """
        if not nombre or not nombre.strip():
            return False, "El nombre del producto no puede estar vacío."
        nombre = nombre.strip()
        if any(char.isdigit() for char in nombre):
            return False, "El nombre del producto no puede contener números."
        if not all(char.isalpha() or char.isspace() for char in nombre):
            return False, "El nombre del producto no puede contener signos especiales."
        return True, ""

    def validar_cantidad(self, cantidad_text):
        """Valida que la cantidad sea un número entero positivo.
        
        Returns:
            Tupla (es_valido: bool, valor_o_error: int o str)
        """
        if not cantidad_text.strip():
            return False, "La cantidad no puede estar vacía."
        try:
            cantidad = int(cantidad_text.strip())
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor que 0."
            return True, cantidad
        except ValueError:
            return False, "La cantidad debe ser un número entero válido."

    def validar_precio(self, precio_text):
        """Valida que el precio sea un número positivo.
        
        Validaciones:
        - Debe ser un número válido (no letras)
        - No puede contener signos especiales
        - Debe ser mayor que 0
        
        Returns:
            Tupla (es_valido: bool, valor_o_error: float o str)
        """
        try:
            precio = float(precio_text.strip())
        except ValueError:
            return False, "El precio debe ser un número válido (no se permiten letras)."
        if precio <= 0:
            return False, "El precio debe ser mayor que 0 (no se permiten valores iguales o menores a 0)."
        return True, precio

    def agregar_producto(self, nombre, cantidad, precio):
        """Agrega un nuevo producto al inventario.
        
        Args:
            nombre: Nombre del producto (ya validado)
            cantidad: Cantidad disponible (número positivo)
            precio: Precio unitario (número positivo)
        
        Returns:
            True si se agregó correctamente
        """
        codigo = self.generar_codigo()
        nuevo_item = {
            'codigo': codigo,
            'producto': nombre,
            'cantidad': cantidad,
            'precio': precio
        }
        self.lista_inventario.append(nuevo_item)
        self.almacenamiento.guardar_inventario(self.lista_inventario)
        return True

    def actualizar_producto(self, codigo, nombre, cantidad, precio):
        """Actualiza los datos de un producto existente.
        
        Args:
            codigo: Código del producto a actualizar
            nombre: Nuevo nombre
            cantidad: Nueva cantidad
            precio: Nuevo precio
        
        Returns:
            True si se encontró y actualizó, False si no existe
        """
        for item in self.lista_inventario:
            if item['codigo'] == codigo:
                item['producto'] = nombre
                item['cantidad'] = cantidad
                item['precio'] = precio
                self.almacenamiento.guardar_inventario(self.lista_inventario)
                return True
        return False

    def eliminar_producto(self, codigo):
        """Elimina un producto del inventario por su código.
        
        Args:
            codigo: Código del producto a eliminar
        """
        self.lista_inventario = [item for item in self.lista_inventario if item['codigo'] != codigo]
        self.almacenamiento.guardar_inventario(self.lista_inventario)

    def buscar_productos(self, criterio):
        """Busca productos por código o nombre (búsqueda parcial).
        
        Si el criterio está vacío, retorna todo el inventario.
        
        Args:
            criterio: Texto a buscar (sin importar mayúsculas/minúsculas)
        
        Returns:
            Lista de productos que coinciden con el criterio
        """
        criterio = criterio.strip().lower()
        if not criterio:
            return self.lista_inventario
        return [item for item in self.lista_inventario if criterio in item['codigo'].lower() or criterio in item['producto'].lower()]

    def resetear_inventario(self):
        """Resetea el inventario a los 5 productos por defecto originales.
        
        Borra todos los cambios y vuelve al estado inicial.
        """
        self.lista_inventario = self._inventario_por_defecto()
        self.almacenamiento.guardar_inventario(self.lista_inventario)

    def generar_reporte(self):
        """Genera un reporte de texto con todos los productos del inventario.
        
        Returns:
            String con el contenido del reporte
        """
        contenido = 'Reporte de inventario\n'
        contenido += '====================\n'
        for item in self.lista_inventario:
            contenido += f"{item['codigo']} - {item['producto']} - Cantidad: {item['cantidad']} - Precio: {item['precio']}\n"
        return contenido

    def _inventario_por_defecto(self):
        """Retorna los 5 productos iniciales del inventario."""
        return [
            {'codigo': '001', 'producto': 'Arroz', 'cantidad': 50, 'precio': 1200},
            {'codigo': '002', 'producto': 'Azúcar', 'cantidad': 30, 'precio': 1500},
            {'codigo': '003', 'producto': 'Aceite', 'cantidad': 20, 'precio': 3500},
            {'codigo': '004', 'producto': 'Leche', 'cantidad': 40, 'precio': 1800},
            {'codigo': '005', 'producto': 'Pan', 'cantidad': 25, 'precio': 2200},
        ]
