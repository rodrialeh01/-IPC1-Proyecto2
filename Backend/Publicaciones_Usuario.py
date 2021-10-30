class Publicaciones_Usuario:
    def __init__(self, usuario, cantidad):
        self.usuario = usuario
        self.cantidad = cantidad

    def getUsuario(self):
        return self.usuario

    def setUsuario(self,usuario):
        self.usuario = usuario

    def getCantidad(self):
        return self.cantidad

    def setCantidad(self, cantidad):
        self.cantidad = cantidad