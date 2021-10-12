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

Usuarios.append(Usuario("Abner Cardona","M","admin","admin@ipc1.com","admin@ipc1"))

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
                nuevo = Usuario(nombre,genero,user,email,contraseña)
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
        for i in range(len(Usuarios)):
            if str(nusuario) == str(Usuarios[i].getUser()):
                validar =True
            else:
                validar =False
        return validar

#METODO PARA VERIFICAR LA LONGITUD DE LA CONTRASEÑA
def cantidadpassword(passw):
    if len(passw) >=8:
        return True
    else:
        return False

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

#Hace que se levante la api que se esta creando
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)