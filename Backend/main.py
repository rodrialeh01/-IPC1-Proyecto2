#Se importan las librerias correspondientes
from typing import List
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

#Llamar a las clases
from Usuario import Usuario
from Publicacion import Publicacion
from Propio import Propio
from Publicaciones_Usuario import Publicaciones_Usuario
from Reaccion import Reaccion

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

#Se crea una lista de cantidad de publicaciones por usuario
CPubsUser = []

#Se crea una lista de reaciones de las publicaciones ("me gusta")
Reacciones = []

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
    global CPubsUser
    try:
        nombre = request.json['name']
        genero = request.json['gender']
        user = request.json['username']
        email = request.json['email']
        contraseña = request.json['password']
        if VerificarUsuario(user) == False:
            if VerificarPassword(contraseña) == True:
                    nuevo = Usuario(nombre,genero.upper(),user,email,contraseña)
                    Usuarios.append(nuevo)
                    CPubsUser.append(Publicaciones_Usuario(nuevo.getUser(),0))
                    return jsonify({'Mensaje': 'Se agregó el usuario correctamente','estado':'true'})
            else:
                return jsonify({'Mensaje': 'Su contraseña debe ser mayor a 8 caracteres, contener un número y un símbolo','estado':'false'})               
        else:
            return jsonify({'Mensaje': 'Ingrese un usuario existente','estado':'false'})
    except:
        return jsonify({'Mensaje': 'No se pudo registrar al usuario','estado':'false'})

#VERIFICAR SI LA CONTRASEÑA ES VALIDA
def VerificarPassword(passwd):
    SpecialSym =['$', '@', '#', '%','!','&','(',')','*','+',',','-','_','.','/',':',';','<','=','>','?','[',']','^','{','}','|']
    val = True
    if len(passwd) < 8:
        print('Ingresa una contraseña mayor a 8 caracteres')
        val = False
        
    if not any(char.isdigit() for char in passwd):
        print('La contraseña debe de tener almenos un numero')
        val = False
        
    if not any(char in SpecialSym for char in passwd):
        print('La contraseña debe de contener almenos un simbolo')
        val = False

    if val:
        return val

#METODO PARA VERIFICAR SI EL USUARIO EXISTE
def VerificarUsuario(nusuario):
    global Usuarios
    validar = False
    for Usuario in Usuarios:
        if str(nusuario) == str(Usuario.getUser()):
            validar =True
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
    global Usuarios
    username = request.json['username']
    password = request.json['password']
    for Usuario in Usuarios:
        if (username=="admin" and password =="admin@ipc1"):
            return jsonify({'Mensaje':'Bienvenido Administrador','Tipo':'Administrador','Login':'true'})
        elif VerificarUsuarios(username,password) == True:
            return jsonify({'Mensaje':'Bienvenido ' + username,'Tipo':'Usuario','Login':'true','user': username})
    return jsonify({'Mensaje':'Credenciales Incorrectas','Tipo':'Error Effesinda', 'Login':'false'})


#METODO PARA VERIFICAR SI EL USUARIO EXISTE
def VerificarUsuarios(us,contra):
    global Usuarios
    validar=False
    for Usuario in Usuarios:
        if (str(Usuario.getUser()) == str(us)):
            if (str(contra)==str(Usuario.getContraseña())):
                validar = True
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
            if VerificarPassword(request.json['password']) == True:
                Usuarios[i].setUser(nusuario)
                Usuarios[i].setNombre(nombre)
                Usuarios[i].setGenero(genero.upper())
                Usuarios[i].setCorreo(correo)
                Usuarios[i].setContraseña(contraseña)
                ActualizarUPropio(usuario,nusuario)
                Actualizarautor(usuario,nusuario)
                Actualizaruscant(usuario,nusuario)
                return jsonify({'Mensajea':'Se actulizó correctamente el usuario','Mensaje':'Se actulizó correctamente el usuario, inicia sesión de nuevo.','estado':'true'})
            else:
                return jsonify({'Mensajea':'Su contraseña debe ser mayor a 8 caracteres, contener un número y un símbolo','estado':'false'})
    return jsonify({'Mensajea': 'No se encontró el usuario','estado':'false'})

#ACTUALIZAR USUARIO EN PROPIO
def ActualizarUPropio(user, nuser):
    global Propios
    for pro in Propios:
        if (str(user) == str(pro.getUsuario())):
            pro.setUsuario(nuser)
            break

#ACTUALIZAR AUTOR DE LA PUBLICACION
def Actualizarautor(user, nuser):
    global Publicaciones
    for pu in Publicaciones:
        if(str(user) == str(pu.getUsuario())):
            pu.setUsuario(nuser)

#ACTUALIZAR LISTADO DE CANTIDAD DE PUBLICACIONES
def Actualizaruscant(user,nuser):
    global CPubsUser
    for cp in CPubsUser:
        if(str(user) == str(cp.getUsuario())):
            cp.setUsuario(nuser)

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

#METODO PARA LA CARGA MASIVA DE USUARIOS
@app.route('/Usuarios/CargaMasiva', methods=['POST'])
def CargaUsuarios():
    global Usuarios
    global CPubsUser
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
            CPubsUser.append(Publicaciones_Usuario(nuevo.getUser(),0))
        else:
            return(jsonify({'Mensaje':'Este usuario ya existe'}))
    return(jsonify({'Mensaje':'Se cargo correctamente'}))

#METODO PARA LA CARGA MASIVA DE PUBLICACIONES
@app.route('/Publicaciones/CargaMasiva', methods=['POST'])
def CargarPublicaciones():
    global Publicaciones
    global Propios
    global CPubsUser
    global PubUser
    global Reacciones
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
            PubUser.append(nuevoi)
            AsignarCantidadP(nuevoi.getUsuario())
            Reacciones.append(Reaccion(nuevoi.getId(),0))
            Propios.append(Propio(authori,PubUser))
        videos = i.get('videos')
        for k in videos:
            m= len(Publicaciones)+1
            urlv = k.get('url')
            datev = k.get('date')
            categoryv = k.get('category')
            authorv = k.get('author')
            nuevov = Publicacion(m,"Video",authorv,urlv,datev,categoryv)
            Publicaciones.append(nuevov)
            AsignarCantidadP(nuevov.getUsuario())
            PubUser.append(nuevov)
            Reacciones.append(Reaccion(nuevov.getId(),0))
            Propios.append(Propio(authorv,PubUser))
    return(jsonify({'Mensaje':'Se hizo correctamente la carga'}))

#ASIGNA LA CANTIDAD DE PUBLICACIONES POR CADA USUARIO
def AsignarCantidadP(pubu):
    global CPubsUser
    for pu in CPubsUser:
        if (str(pubu) == str(pu.getUsuario())):
            aumento = int(pu.getCantidad()) +1
            pu.setCantidad(int(aumento))
            break

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
            descontarPubs(Publicaciones[i].getUsuario())
            eliminarpubuser(Publicaciones[i].getId(), Publicaciones[i].getUsuario())
            del Publicaciones[i]            
            return jsonify({'Mensaje':'Se eliminó la publicacion exitosamente'})
    return jsonify({'Mensaje':'No se encontró la publicacion'})

#Se descuenta la publicacion eliminada por el administrador
def descontarPubs(user):
    global CPubsUser
    for pu in CPubsUser:
        if (str(user) == str(pu.getUsuario())):
            descuento = int(pu.getCantidad()) -1
            pu.setCantidad(int(descuento))

#Eliminar la publicacion asignada al usuario
def eliminarpubuser(idp, user):
    global PubUser
    global Propios
    Datos = []
    for i in PubUser:
        if(int(idp) == int(i.getId())):
            PubUser.remove(i)
    for p in Propios:
        if(p.getUsuario() == user):
            p.setPublicacion(PubUser)

#METODO PARA RETORNAR LAS PUBLICACIONES Y MOSTRARLAS EN EL BACKEND DE INICIO
@app.route('/Publicaciones/Inicio', methods=['GET'])
def PublicacionesInicio():
    global Publicaciones
    Datos = []
    for i in range(len(Publicaciones)):
        objeto = {
            'id': Publicaciones[i].getId(),
            'type': Publicaciones[i].getTipo(),
            'username': Publicaciones[i].getUsuario(),
            'date': Publicaciones[i].getFecha(),
            'category': Publicaciones[i].getCategoria(),
            'url': Publicaciones[i].getUrl(),
            'likes': likespub(Publicaciones[i].getId())
        }
        Datos.append(objeto)
    return(jsonify(Datos))

#PUBLICAR UN POST
@app.route('/Publicaciones/Nuevo', methods=['POST'])
def NuevoPost():
    global Publicaciones
    global Propios
    global PubUser
    global CPubsUser
    username = request.json['username']
    type = request.json['type']
    date = request.json['date']
    category = request.json['category']
    url = request.json['url']
    if username != "" and type != "" and date != "" and category != "" and url != "":
        nuevo = Publicacion((ultimap()+1),type,username,url,date,category)
        Publicaciones.append(nuevo)
        PubUser.append(nuevo)
        AsignarCantidadP(username)
        Propios.append(Propio(username,PubUser))
        Reacciones.append(Reaccion(nuevo.getId(),0))
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
                        'id': pub.getId(),
                        'type': pub.getTipo(),
                        'username': pub.getUsuario(),
                        'date': pub.getFecha(),
                        'category': pub.getCategoria(),
                        'url':pub.getUrl(),
                        'likes': likespub(pub.getId())
                    }
                    Publis.append(objeto)
            OrdenamientoReacciones(Publis)
            objeto = {
                'username': Propio.getUsuario(),
                'publicacion': Publis
            }
    return(jsonify(objeto))

#RETORNAR LA CANTIDAD DE LIKES DE LA PUBLICACION
def likespub(idp):
    global Reacciones
    for i in range(len(Reacciones)):
        if(int(idp) == int(Reacciones[i].getIdpublicacion())):
            return(Reacciones[i].getCantidad())

#OBTENER REACCIONES
@app.route('/Reacciones', methods=['GET'])
def obtenerreacciones():
    global Reacciones
    OrdenamientoReacciones(Reacciones)
    Datos = []
    for r in Reacciones:
        objeto = {
            'id': r.getIdpublicacion(),
            'likes': r.getCantidad()
        }
        Datos.append(objeto)
    return(jsonify(Datos))

#OBTENER EL TOP 5 DE PUBLICACIONES CON MÁS REACCIONES
@app.route('/Publicaciones/Reacciones', methods=['GET'])
def ObtenerTopReacciones():
    global Reacciones
    Datos = []
    OrdenamientoReacciones(Reacciones)
    objeto0 = {
        'id': Reacciones[0].getIdpublicacion(),
        'likes': Reacciones[0].getCantidad()
    }
    Datos.append(objeto0)
    objeto1 = {
        'id': Reacciones[1].getIdpublicacion(),
        'likes': Reacciones[1].getCantidad()
    }
    Datos.append(objeto1)
    objeto2 = {
        'id': Reacciones[2].getIdpublicacion(),
        'likes': Reacciones[2].getCantidad()
    }
    Datos.append(objeto2)
    objeto3 = {
        'id': Reacciones[3].getIdpublicacion(),
        'likes': Reacciones[3].getCantidad()
    }
    Datos.append(objeto3)
    objeto4 = {
        'id': Reacciones[4].getIdpublicacion(),
        'likes': Reacciones[4].getCantidad()
    }
    Datos.append(objeto4)
    return(jsonify(Datos))

#ORDENAMIENTO DE REACCIONES DE LIKES
def OrdenamientoReacciones(arreglo):
    try:
        for i in range(1,len(arreglo)):
            clave = arreglo[i]
            j = i-1
            while (j>=0 and arreglo[j].getCantidad() < clave.getCantidad()):
                arreglo[j+1] = arreglo[j]
                j = j-1
            arreglo[j+1] = clave
        return(arreglo)
    except:
        print('F')

#RETORNA LA CANTIDAD DE PUBLICACIONES POR CADA USUARIO
@app.route('/Publicaciones/Usuarios', methods=['GET'])
def ObtenerPUsers():
    global CPubsUser
    Datos = []
    OrdenamientoCPublicaciones(CPubsUser)
    objeto0 = {
        'username': CPubsUser[0].getUsuario(),
        'cantidad': CPubsUser[0].getCantidad()
    }
    Datos.append(objeto0)
    objeto1 = {
        'username': CPubsUser[1].getUsuario(),
        'cantidad': CPubsUser[1].getCantidad()
    }
    Datos.append(objeto1)
    objeto2 = {
        'username': CPubsUser[2].getUsuario(),
        'cantidad': CPubsUser[2].getCantidad()
    }
    Datos.append(objeto2)
    objeto3 = {
        'username': CPubsUser[3].getUsuario(),
        'cantidad': CPubsUser[3].getCantidad()
    }
    Datos.append(objeto3)
    objeto4 = {
        'username': CPubsUser[4].getUsuario(),
        'cantidad': CPubsUser[4].getCantidad()
    }
    Datos.append(objeto4)
    return(jsonify(Datos))

#ORDENAMIENTO DE CANTIDAD DE PUBLICACIONES
def OrdenamientoCPublicaciones(arreglo):
    try:
        for i in range(1,len(arreglo)):
            clave = arreglo[i]
            j = i-1
            while (j>=0 and arreglo[j].getCantidad() < clave.getCantidad()):
                arreglo[j+1] = arreglo[j]
                j = j-1
            arreglo[j+1] = clave
        return(arreglo)
    except:
        print('F')

#AÑADIR 1 REACCION A 1 PUBLICACION
@app.route('/Reaccion/Añadir', methods=['POST'])
def Añadirlike():
    global Reacciones
    id = request.json['id']
    like = request.json['like']
    if(like =="True"):
        AumentarLikes(id)
        return(jsonify({'Mensaje':'Se dio like a la publicacion'}))

#AUMENTAR LA CANTIDAD DE LIKES
def AumentarLikes(idp):
    global Reacciones
    for re in Reacciones:
        if (int(idp) == int(re.getIdpublicacion())):
            aumento = int(re.getCantidad()) +1
            re.setCantidad(int(aumento))
            break

#Hace que se levante la api que se esta creando
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)