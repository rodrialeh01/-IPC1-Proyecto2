class Propio:
    def __init__(self, usuario, publicacion):
        self.usuario = usuario
        self.publicacion = publicacion

    def getUsuario(self):
        return self.usuario
    
    def setUsuario(self, usuario):
        self.usuario = usuario
    
    def getPublicacion(self):
        return self.publicacion

    def setPublicacion(self,publicacion):
        self.publicacion = publicacion