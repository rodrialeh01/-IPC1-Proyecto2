class Reaccion:
    def __init__(self, idpublicacion, cantidad):
        self.idpublicacion = idpublicacion
        self.cantidad = cantidad

    def getIdpublicacion(self):
        return self.idpublicacion

    def setIdpublicacion(self,idpublicacion):
        self.idpublicacion = idpublicacion

    def getCantidad(self):
        return self.cantidad

    def setCantidad(self, cantidad):
        self.cantidad = cantidad