class Usuario:
    #CONSTRUCTOR
    def __init__(self,nombre, genero, user, correo, contraseña):
        self.nombre = nombre
        self.genero = genero
        self.user = user
        self.correo = correo
        self.contraseña = contraseña

    #ENCAPSULAMIENTO
    def getNombre(self):
        return self.nombre
    
    def setNombre(self, nombre):
        self.nombre = nombre

    def getGenero(self):
        return self.genero
    
    def setGenero(self, genero):
        self.genero = genero

    def getUser(self):
        return self.user
    
    def setUser(self, user):
        self.user = user

    def getCorreo(self):
        return self.correo
    
    def setCorreo(self, correo):
        self.correo = correo

    def getContraseña(self):
        return self.contraseña
    
    def setContraseña(self, contraseña):
        self.contraseña = contraseña