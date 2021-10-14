#Se importan las librerias correspondientes
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

#Llamar a la clase
from Usuario import Usuario

# se crea una variable para poder crear la API
app = Flask(__name__)
CORS(app)

#Se crea una lista de usuarios
Usuarios = []
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
                if genero == "M" or genero =="F" or genero=="m" or genero=="f":
                    nuevo = Usuario(nombre,genero.upper(),user,email,contraseña)
                    Usuarios.append(nuevo)
                    return jsonify({'Mensaje': 'Se agregó el usuario correctamente'})
                else:
                    return jsonify({'Mensaje': 'Unicamente puede poner "M", "m", "F" o "f" en el genero'})
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
        for i in range(len(Usuarios)):
            if str(nusuario) == str(Usuarios[i].getUser()):
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
@app.route('/Login',methods=['POST'])
def VerificarCredenciales():
    usuario = request.json['user']
    contraseña = request.json['password']
    if usuario=="admin" and contraseña =="admin@ipc1":
        return jsonify({'Mensaje':'Bienvenido Administrador','Tipo':'Administrador','Login':'true'})
    elif VerificarUsuarios(usuario,contraseña)==True:
        return jsonify({'Mensaje':'Bienvenido ' + usuario,'Tipo':'Usuario','Login':'true'})
    else:
        return jsonify({'Mensaje':'Credenciales Incorrectas','Tipo':'Error', 'Login':'false'})

#METODO PARA VERIFICAR SI EL USUARIO EXISTE
def VerificarUsuarios(us,contra):
    global Usuarios
    for i in range(len(Usuarios)):
        if us==Usuarios[i].getUser() and contra==Usuarios[i].getContraseña():
            validar = True
        else:
            validar = False
    return validar

#MODIFICAR UN USUARIO
@app.route('/Usuarios/Modificar/<string:user>',methods=['PUT'])
def ActualizarUsuario(user):
    global Usuarios
    nombre = request.json['name']
    genero = request.json['gender']
    correo = request.json['email']
    contraseña = request.json['password']
    for i in range(len(Usuarios)):
        if str(user) == str(Usuarios[i].getUser()):
            if cantidadpassword(contraseña) == True:
                if genero == "M" or genero =="F" or genero=="m" or genero=="f":
                    Usuarios[i].setNombre(nombre)
                    Usuarios[i].setGenero(genero)
                    Usuarios[i].setCorreo(correo)
                    Usuarios[i].setContraseña(contraseña)
                    return jsonify({'Mensaje':'Se actulizó correctamente el usuario'})
                else:
                    return jsonify({'Mensaje': 'Unicamente puede poner "M", "m", "F" o "f" en el genero'})
            else:
                return jsonify({'Mensaje': 'Su contraseña debe ser mayor a 8 caracteres'})
        else:
            return jsonify({'Mensaje': 'No se encontró el usuario'})

#METODO PARA RETORNAR 1 USUARIO
@app.route('/Usuarios/<string:user>', methods=['GET'])
def RetornarUsuario(user):
    global Usuarios
    for Usuario in Usuarios:
        if Usuario.getUser():
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
    publis = request.json['publicaciones']
    listap = json.loads(publis)
    for i in listap:
        imagenes = i.get('images')
        for j in imagenes:
            print("Tipo: Imagen")
            print("URL: ", j.get('url'))
            print("Fecha: ", j.get('date'))
            print("Categoria: ", j.get('category'))
        videos = i.get('videos')
        for k in videos:
            print("Tipo: Video")
            print("URL: ", k.get('url'))
            print("Fecha: ", k.get('date'))
            print("Categoria: ", k.get('category'))
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

#Hace que se levante la api que se esta creando
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)