function DatosP(){
    var tabla = document.querySelector('#contenidopublicaciones')
    var cadena =''

    fetch('http://localhost:3000/Publicaciones/Tabla', {
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
        cadena += `<tr width="100%">
            <td> ${element.id} </td>
            <td> ${element.tipo} </td>
            <td> ${element.username} </td>
            <td> ${element.date} </td>
            <td> ${element.category} </td>
            <td><div class="card-body text-primary" style="width: 20rem;">${element.url}</div></td>
            <td> <button value=${element.id} type="button" onclick="verPublicacion(this)" class="btn btn-info btn-sm"><i class="material-icons">visibility</i></button> <button value=${element.id} onclick="actualizarPublicacion(this)" type="button" class="btn btn-success btn-sm"><i class="material-icons">edit</i></button> <button value=${element.id} onclick="eliminarPublicacion(this)" type="button" class="btn btn-danger btn-sm"><i class="material-icons">delete</i></button> </td>
            </tr>`        
        });
        tabla.innerHTML = cadena
      })
  }

  function verPublicacion(boton1){
    console.log(boton1)
    var publi = boton1.value

    sessionStorage.setItem("verp", publi)

    location.href="PublicacionVer.html"
  }

  function actualizarPublicacion(boton2){
    console.log(boton2)
    var publi = boton2.value

    sessionStorage.setItem("editp", publi)

    location.href="PublicacionEditar.html"
  }

  function eliminarPublicacion(boton3){
    console.log(boton3)
    var idp = boton3.value

    fetch(`http://localhost:3000/Publicaciones/Eliminar/${idp}`, {
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
                location.href="TablaPublicaciones.html"
            })
  }

  DatosP();