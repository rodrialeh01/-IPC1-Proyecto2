class Publicacion:
    #CONSTRUCTOR
    def __init__(self,id, tipo, usuario, url, fecha, categoria):
        self.id = id
        self.tipo = tipo
        self.usuario = usuario
        self.url = url
        self.fecha = fecha
        self.categoria = categoria

    #ENCAPSULAMIENTO
    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getUsuario(self):
        return self.usuario

    def setUsuario(self,usuario):
        self.usuario = usuario

    def getUrl(self):
        return self.url

    def setUrl(self,url):
        self.url = url

    def getFecha(self):
        return self.fecha

    def setFecha(self,fecha):
        self.fecha = fecha

    def getCategoria(self):
        return self.categoria

    def setCategoria(self,categoria):
        self.categoria = categoria