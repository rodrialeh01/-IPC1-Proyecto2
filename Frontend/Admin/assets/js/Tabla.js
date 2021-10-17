function DatosU(){
    var tabla = document.querySelector('#contenidousers')
    var cadena =''

    fetch('http://localhost:3000/Usuarios/Tabla', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    })
      .then(res => res.json())
      .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
      })
      .then(response => {
        console.log(response);
        response.forEach(element => {
          console.log(element)
          if(element.username !="admin"){
            cadena += `<tr>
            <td> ${element.no} </td>
            <td> ${element.name} </td>
            <td> ${element.username} </td>
            <td> ${element.email} </td>
            <td> ${element.gender} </td>
            <td> ${element.password} </td>            
            <td> <button value=${element.username} onclick="verPerfil(this)" type="button" class="btn btn-info btn-sm"><i class="material-icons">visibility</i></button> <button value=${element.username} onclick="actualizarPerfil(this)" type="button" class="btn btn-success btn-sm"><i class="material-icons">edit</i></button> <button value=${element.username} onclick="eliminarPerfil(this)" type="button" class="btn btn-danger btn-sm"><i class="material-icons">delete</i></button></td>
            </tr>`
          }          
        });
        tabla.innerHTML = cadena
      })
  }

  function verPerfil(boton1){
    console.log(boton1)
    var usuario = boton1.value

    sessionStorage.setItem("ver", usuario)

    location.href="UsuarioVer.html"
  }

  function actualizarPerfil(boton2){
    console.log(boton2)
    var usuario = boton2.value

    sessionStorage.setItem("edit", usuario)

    location.href="UsuarioEditar.html"
  }

  function eliminarPerfil(boton3){
    console.log(boton3)
    var usuario = boton3.value

    fetch(`http://localhost:3000/Usuarios/Eliminar/${usuario}`, {
            method: 'DELETE',
            headers:{
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',}})
            .then(res => res.json())
            .catch(err => {
                console.error('Error:', err)
                alert("Ocurrio un error, ver la consola")
            })
            .then(response =>{
                console.log(response);
                alert(response.Mensaje)
                location.href="TablaUsers.html"
            })
  }
  DatosU();