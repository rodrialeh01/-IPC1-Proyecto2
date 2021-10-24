#Se importan las librerias correspondientes
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

#Llamar a las clases
from Usuario import Usuario
from Publicacion import Publicacion
from Propio import Propio

# se crea una variable para poder crear la API
app = Flask(__name__)
CORS(app)

#Se crea una lista de usuarios
Usuarios = []

#Se crea una lista de publicaciones
Publicaciones = []

#Se crea una lista de Publicaciones para asignarlas a Propios
PubUser = []

#Se crea una lista de Propio para asignar las publicaciones
Propios = []
#Se define al usuario Administrador
Usuarios.append(Usuario("Abner Cardona","M","admin","admin@ipc1.com","admin@ipc1"))

#METODO PARA MOSTRAR AL INICIO DEL BACKEND
@app.route('/',methods=['GET'])
def Inicio():
    return("<h1>Backend U-Blog</h1>")

#METODO PARA CREAR USUARIOS
@app.route('/Usuarios/Registrar', methods=['POST'])
def RegistrarUsuario():
    global Usuarios
    try:
        nombre = request.json['name']
        genero = request.json['gender']
        user = request.json['username']
        email = request.json['email']
        contraseña = request.json['password']
        if VerificarUsuario(user) == False:
            if cantidadpassword(contraseña) == True:
                    nuevo = Usuario(nombre,genero.upper(),user,email,contraseña)
                    Usuarios.append(nuevo)
                    return jsonify({'Mensaje': 'Se agregó el usuario correctamente'})
            else:
                return jsonify({'Mensaje': 'Su contraseña debe ser mayor a 8 caracteres'})               
        else:
            return jsonify({'Mensaje': 'Ingrese un usuario existente'})
    except:
        return jsonify({'Mensaje': 'No se pudo registrar al usuario'})

#METODO PARA VERIFICAR SI EL USUARIO EXISTE
def VerificarUsuario(nusuario):
    global Usuarios
    if len(Usuarios)==0:
        return False        
    else:
        for Usuario in Usuarios:
            if str(nusuario) == str(Usuario.getUser()):
                validar =True
            else:
                validar =False
        return validar

#METODO PARA VER LOS USUARIOS
@app.route('/Usuarios', methods=['GET'])
def MostrarUsuarios():
    global Usuarios
    Datos = []
    for Usuario in Usuarios:
        objeto = {
            'name':Usuario.getNombre(),
            'gender':Usuario.getGenero(),
            'username':Usuario.getUser(),
            'email':Usuario.getCorreo(),
            'password':Usuario.getContraseña()
        }
        Datos.append(objeto)
    return(jsonify(Datos))

#METODO PARA VER Y RETORNAR LOS USUARIOS CON SU CONTADOR
@app.route('/Usuarios/Tabla', methods=['GET'])
def MostrarUsuariosT():
    global Usuarios
    Datos = []
    for i in range(len(Usuarios)):
        objeto = {
            'no': i,
            'name':Usuarios[i].getNombre(),
            'gender':Usuarios[i].getGenero(),
            'username':Usuarios[i].getUser(),
            'email':Usuarios[i].getCorreo(),
            'password':Usuarios[i].getContraseña()
        }
        Datos.append(objeto)
    return(jsonify(Datos))

#VERIFICAR LOGIN
@app.route('/Login/<string:username>/<string:password>',methods=['GET'])
def VerificarCredenciales(username,password):
    global Usuarios
    for Usuario in Usuarios:
        if (username=="admin" and password =="admin@ipc1"):
            return jsonify({'Mensaje':'Bienvenido Administrador','Tipo':'Administrador','Login':'true'})
        elif str(Usuario.getUser()) == str(username) and str(Usuario.getContraseña()) == str(password):
            return jsonify({'Mensaje':'Bienvenido ' + username,'Tipo':'Usuario','Login':'true','user': username})
        else:
            return jsonify({'Mensaje':'Credenciales Incorrectas','Tipo':'Error Effesinda', 'Login':'false'})


#METODO PARA VERIFICAR SI EL USUARIO EXISTE
def VerificarUsuarios(us,contra):
    global Usuarios
    for Usuario in Usuarios:
        if ((str(Usuario.getUser()) == str(us)) and (str(contra)==str(Usuario.getContraseña()))):
            validar = True
        else:
            validar = False
    return validar

#MODIFICAR UN USUARIO
@app.route('/Usuarios/Modificar/<string:usuario>',methods=['PUT'])
def ActualizarUsuario(usuario):
    global Usuarios
    nusuario = request.json['username']
    nombre = request.json['name']
    genero = request.json['gender']
    correo = request.json['email']
    contraseña = request.json['password']
    for i in range(len(Usuarios)):
        if usuario == Usuarios[i].getUser():
            if cantidadpassword(request.json['password']) == True:
                Usuarios[i].setUser(nusuario)
                Usuarios[i].setNombre(nombre)
                Usuarios[i].setGenero(genero.upper())
                Usuarios[i].setCorreo(correo)
                Usuarios[i].setContraseña(contraseña)
                return jsonify({'Mensaje':'Se actulizó correctamente el usuario'})
            else:
                return jsonify({'Mensaje':'Su contraseña debe ser mayor a 8 caracteres'})
    return jsonify({'Mensaje': 'No se encontró el usuario'})

#METODO PARA RETORNAR 1 USUARIO
@app.route('/Usuarios/<string:user>', methods=['GET'])
def RetornarUsuario(user):
    global Usuarios
    for Usuario in Usuarios:
        if str(Usuario.getUser()) == str(user):
            objeto = {
                'name': Usuario.getNombre(),
                'user': Usuario.getUser(),
                'password': Usuario.getContraseña(),
                'gender': Usuario.getGenero(),
                'email': Usuario.getCorreo()
            }
            return(jsonify(objeto))
    return(jsonify({'Mensaje':'No se encuentra el usuario'}))

#METODO PARA VERIFICAR LA LONGITUD DE LA CONTRASEÑA
def cantidadpassword(passw):
    if len(passw) >=8:
        return True
    else:
        return False

#METODO PARA LA CARGA MASIVA DE USUARIOS
@app.route('/Usuarios/CargaMasiva', methods=['POST'])
def CargaUsuarios():
    users = request.json['users']
    listau = json.loads(users)
    for usu in listau:
        name = usu.get('name')
        gender = usu.get('gender')
        username = usu.get('username')
        email = usu.get('email')
        passw = usu.get('password')
        if VerificarUsuario(username) == False:
            nuevo = Usuario(name,gender.upper(),username,email,passw)
            Usuarios.append(nuevo)
        else:
            return(jsonify({'Mensaje':'Este usuario ya existe'}))
    return(jsonify({'Mensaje':'Se cargo correctamente'}))

#METODO PARA LA CARGA MASIVA DE PUBLICACIONES
@app.route('/Publicaciones/CargaMasiva', methods=['POST'])
def CargarPublicaciones():
    global Publicaciones
    global Propios
    DPub = []
    publis = request.json['publicaciones']
    listap = json.loads(publis)
    for i in listap:
        imagenes = i.get('images')
        for j in imagenes:
            l= len(Publicaciones) +1
            urli = j.get('url')
            datei = j.get('date')
            categoryi = j.get('category')
            authori = j.get('author')
            nuevoi = Publicacion(l,"Imagen",authori,urli,datei,categoryi)
            Publicaciones.append(nuevoi)
            DPub.append(nuevoi)
            Propios.append(Propio(authori,DPub))
        videos = i.get('videos')
        for k in videos:
            m= len(Publicaciones)+1
            urlv = k.get('url')
            datev = k.get('date')
            categoryv = k.get('category')
            authorv = k.get('author')
            nuevov = Publicacion(m,"Video",authorv,urlv,datev,categoryv)
            Publicaciones.append(nuevov)
            DPub.append(nuevov)
            Propios.append(Propio(authorv,DPub))
    return(jsonify({'Mensaje':'Se hizo correctamente la carga'}))

#METODO PARA ELIMINAR UN USUARIO
@app.route('/Usuarios/Eliminar/<string:user>',methods=['DELETE'])
def EliminarUsuario(user):
    global Usuarios
    for i in range(len(Usuarios)):
        if user == Usuarios[i].getUser():
            del Usuarios[i]
            return jsonify({'Mensaje':'Se eliminó el usuario exitosamente'})
    return jsonify({'Mensaje':'No se encontró el usuario'})

#METODO PARA RETORNAR LA CANTIDAD DE USUARIOS
@app.route('/Usuarios/Contador',methods=['GET'])
def ContadorUsuarios():
    global Usuarios
    contador =len(Usuarios) - 1
    return jsonify({'Cantidad': contador})

#METODO PARA RETORNAR LA CANTIDAD DE PUBLICACIONES
@app.route('/Publicaciones/Contador',methods=['GET'])
def ContadorPublicaciones():
    global Publicaciones
    contadorp = len(Publicaciones)
    return jsonify({'Cantidad': contadorp})

#METODO PARA VER Y RETORNAR LAS PUBLICACIONES CON SU CONTADOR
@app.route('/Publicaciones/Tabla', methods=['GET'])
def MostrarPublicacionesT():
    global Publicaciones
    Datos = []
    for i in range(len(Publicaciones)):
        objeto = {
            'id': Publicaciones[i].getId(),
            'tipo':Publicaciones[i].getTipo(),
            'username': Publicaciones[i].getUsuario(),
            'date':Publicaciones[i].getFecha(),
            'category':Publicaciones[i].getCategoria(),
            'url':Publicaciones[i].getUrl()
        }
        Datos.append(objeto)
    return(jsonify(Datos))

#METODO PARA RETORNAR LA PUBLICACIÓN
@app.route('/Publicaciones/<int:idP>', methods=['GET'])
def VerPublicacion(idP):
    global Publicaciones
    for Publicacion in Publicaciones:
        if str(idP) == str(Publicacion.getId()):
            objetoP = {
                'id':Publicacion.getId(),
                'url': Publicacion.getUrl(),
                'tipo': Publicacion.getTipo(),
                'date': Publicacion.getFecha(),
                'category': Publicacion.getCategoria()
            }
            return jsonify(objetoP)
    return jsonify({'Mensaje':'No se encontro la publicacion'})

#METODO PARA EDITAR LA PUBLICACIÓN
@app.route('/Publicaciones/Modificar/<int:idP>', methods=['PUT'])
def EditarPublicacion(idP):
    global Publicaciones
    fechap = request.json['date']
    categoriap = request.json['category']
    urlp = request.json['url']
    for i in range(len(Publicaciones)):
        if idP == int(Publicaciones[i].getId()):
            Publicaciones[i].setFecha(fechap)
            Publicaciones[i].setCategoria(categoriap)
            Publicaciones[i].setUrl(urlp)
            return jsonify({'Mensaje':'Se actulizó correctamente la publicación'})
    return jsonify({'Mensaje': 'No se encontró la publicación'})

#METODO PARA ELIMINAR LA PUBLICACION
@app.route('/Publicaciones/Eliminar/<int:idP>', methods=['DELETE'])
def EliminarPublicacion(idP):
    global Publicaciones
    for i in range(len(Publicaciones)):
        if idP == Publicaciones[i].getId():
            del Publicaciones[i]
            return jsonify({'Mensaje':'Se eliminó la publicacion exitosamente'})
    return jsonify({'Mensaje':'No se encontró la publicacion'})

#METODO PARA RETORNAR LAS PUBLICACIONES Y MOSTRARLAS EN EL BACKEND DE INICIO
@app.route('/Publicaciones/Inicio', methods=['GET'])
def PublicacionesInicio():
    global Publicaciones
    Datos = []
    for i in range(len(Publicaciones)):
        objeto = {
            'type': Publicaciones[i].getTipo(),
            'username': Publicaciones[i].getUsuario(),
            'date': Publicaciones[i].getFecha(),
            'category': Publicaciones[i].getCategoria(),
            'url': Publicaciones[i].getUrl()
        }
        Datos.append(objeto)
    return(jsonify(Datos))

#PUBLICAR UN POST
@app.route('/Publicaciones/Nuevo', methods=['POST'])
def NuevoPost():
    global Publicaciones
    global Propios
    global PubUser
    username = request.json['username']
    type = request.json['type']
    date = request.json['date']
    category = request.json['category']
    url = request.json['url']
    if username != "" and type != "" and date != "" and category != "" and url != "":
        nuevo = Publicacion((ultimap()+1),type,username,url,date,category)
        Publicaciones.append(nuevo)
        PubUser.append(nuevo)
        Propios.append(Propio(username,PubUser))
        return jsonify({'Mensaje':'Publicación hecha con éxito'})
    return jsonify({'Mensaje': 'No se pudo realizar el POST'})

#OBTENER EL ULTIMO ID DE LAS LISTA DE PUBLICACIONES 
def ultimap():
    global Publicaciones
    return(Publicaciones[len(Publicaciones)-1].getId())

#OBTENER LAS PUBLICACIONES DE CADA USUARIO
@app.route('/Publicaciones/<string:user>', methods=['GET'])
def PublicacionesUsuario(user):
    global Publicaciones
    global Propios
    for Propio in Propios:
        if(Propio.getUsuario()==user):
            Publis = []
            for pub in Propio.getPublicacion():
                if(pub.getUsuario() == user):
                    objeto = {
                        'type': pub.getTipo(),
                        'username': pub.getUsuario(),
                        'date': pub.getFecha(),
                        'category': pub.getCategoria(),
                        'url':pub.getUrl()
                    }
                    Publis.append(objeto)
            objeto = {
                'username': Propio.getUsuario(),
                'publicacion': Publis
            }
    return(jsonify(objeto))

#Hace que se levante la api que se esta creando
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)