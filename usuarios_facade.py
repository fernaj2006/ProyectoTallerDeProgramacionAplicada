from almacenamiento import JsonUsuario
from login_logica import LogicaUsuarios


class UsuariosFacade:
    """Fachada para la gestion de usuarios.

    Patron estructural Facade: simplifica el acceso al sistema de usuarios,
    ocultando a la interfaz grafica los detalles del archivo JSON y la logica
    de autenticacion/registro.
    """

    def __init__(self, archivo_json='usuarios.json'):
        almacenamiento = JsonUsuario(archivo_json)
        self.logica = LogicaUsuarios(almacenamiento)

    def validar_acceso(self, username, password):
        credenciales = {
            'username': username,
            'password': password
        }
        return self.logica.validar_acceso(credenciales)

    def registrar_usuario(self, username, password):
        nuevo_usuario = {
            'username': username,
            'password': password
        }
        return self.logica.registrar_usuario(nuevo_usuario)
