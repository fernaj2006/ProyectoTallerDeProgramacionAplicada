from __future__ import annotations
from abc import ABC, abstractmethod
from fpdf import FPDF


class EstrategiaReporte(ABC):
    """Interfaz abstracta del patrón Strategy.

    Define el contrato que toda estrategia de reporte debe cumplir.
    InventarioFacade trabaja con esta interfaz sin importar el formato concreto.
    """

    @abstractmethod
    def generar(self, inventario: list):
        """Genera el contenido del reporte a partir del inventario.

        Args:
            inventario: Lista de diccionarios con los productos.

        Returns:
            str si el formato es texto plano, bytes si es binario (PDF).
        """
        pass


class ReporteTXT(EstrategiaReporte):
    """Estrategia concreta: genera el reporte en formato TXT.

    Es el comportamiento original del sistema, ahora encapsulado
    como una estrategia intercambiable.
    """

    def generar(self, inventario: list) -> str:
        contenido = 'Reporte de inventario\n'
        contenido += '====================\n'
        for item in inventario:
            contenido += (
                f"{item['codigo']} - {item['producto']} "
                f"- Cantidad: {item['cantidad']} "
                f"- Precio: {item['precio']}\n"
            )
        return contenido


class ReportePDF(EstrategiaReporte):
    """Estrategia concreta: genera el reporte en formato PDF con tabla.

    Requiere la libreria fpdf2:
        pip install fpdf2
    """

    COL_CODIGO   = 30
    COL_PRODUCTO = 80
    COL_CANTIDAD = 35
    COL_PRECIO   = 35
    FILA_ALTO    = 8

    def generar(self, inventario: list) -> bytes:
        pdf = FPDF()
        pdf.add_page()

        # Titulo
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, 'Reporte de Inventario', ln=True, align='C')
        pdf.ln(5)

        # Encabezados con fondo azul oscuro
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_fill_color(52, 73, 94)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(self.COL_CODIGO,   self.FILA_ALTO, 'Codigo',   border=1, align='C', fill=True)
        pdf.cell(self.COL_PRODUCTO, self.FILA_ALTO, 'Producto', border=1, align='C', fill=True)
        pdf.cell(self.COL_CANTIDAD, self.FILA_ALTO, 'Cantidad', border=1, align='C', fill=True)
        pdf.cell(self.COL_PRECIO,   self.FILA_ALTO, 'Precio',   border=1, align='C', fill=True)
        pdf.ln()

        # Filas con color alternado
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        for i, item in enumerate(inventario):
            if i % 2 == 0:
                pdf.set_fill_color(236, 240, 241)
            else:
                pdf.set_fill_color(255, 255, 255)

            pdf.cell(self.COL_CODIGO,   self.FILA_ALTO, str(item['codigo']),   border=1, align='C', fill=True)
            pdf.cell(self.COL_PRODUCTO, self.FILA_ALTO, str(item['producto']), border=1,             fill=True)
            pdf.cell(self.COL_CANTIDAD, self.FILA_ALTO, str(item['cantidad']), border=1, align='C', fill=True)
            pdf.cell(self.COL_PRECIO,   self.FILA_ALTO, f"${item['precio']}",  border=1, align='C', fill=True)
            pdf.ln()

        # Total
        pdf.ln(4)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 8, f"Total de productos: {len(inventario)}", ln=True)

        return pdf.output()